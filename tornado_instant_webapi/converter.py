import json
from typing import Callable, Dict, Optional, Type, TypeVar, Union

T = TypeVar('T', bound=Type)
Encoder = Callable[[bytes], T]
Decoder = Callable[[T], Union[bytes, str]]


def _to_bool(b):
    if b.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif b.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError(b)


class Converter(object):
    """
    Convert the Python object and the request parameter, each other.
    """

    def __init__(self):
        self.types = {}  # type: Dict[str, Type]
        self.encoders = {}  # type: Dict[str, Encoder[T]]
        self.decoders = {}  # type: Dict[str, Decoder[T]]
        self.content_types = {}  # type: Dict[str, Optional[str]]

        self.register_new_type('str', str)
        self.register_new_type('int', int)
        self.register_new_type('bool', bool, lambda o: str(int(o)), _to_bool)
        self.register_new_type('float', float)
        self.register_new_type('tuple', tuple,
                               lambda o: json.dumps(o),
                               lambda b: tuple(json.loads(str(b))),
                               'application/json; charset=UTF-8')
        self.register_new_type('list', list,
                               lambda o: json.dumps(o),
                               lambda b: list(json.loads(str(b))),
                               'application/json; charset=UTF-8')
        self.register_new_type('dict', dict,
                               lambda o: json.dumps(o),
                               lambda b: dict(json.loads(str(b))),
                               'application/json; charset=UTF-8')
        self.register_new_type('none', type(None), lambda o: '')

    def register_new_type(
            self,
            key: str,
            t: Optional[T],
            encoder: Optional[Encoder[T]] = None,
            decoder: Optional[Decoder[T]] = None,
            content_type: Optional[str] = None,
    ):
        """
        Register encoder and decoder for new type.
        :param key: Unique key for type.
        :param t: Type.
        :param encoder: Converter the Python object to the request parameter.
        :param decoder: Converter the request parameter to the Python object.
        :param content_type: `Content-Type` to be used HTTP request.
        """
        assert key not in self.types.keys(), 'Key `{}` is registered.'.format(key)

        if t is not None:
            assert t not in self.types.values(), 'Type `{}` is registered.'.format(t)

        if encoder is None:
            encoder = str  # default encoder

        if decoder is None:
            assert t is not None, 'If decoder is None, t must be given.'
            decoder = t

        self.types[key] = t
        self.encoders[key] = encoder
        self.decoders[key] = decoder
        self.content_types[key] = content_type

    def encode(self, obj, key_or_type: Optional[Union[Type, str]] = None):
        """
        Convert the Python object to the request parameter.
        """
        if key_or_type is None:
            key_or_type = type(obj)
        key = self._get_key(key_or_type)
        return self.encoders[key](obj)

    def decode(self, obj: bytes, key_or_type: Union[Type, str]):
        """
        Convert the request parameter to the Python object.
        """
        key = self._get_key(key_or_type)
        return self.decoders[key](obj)

    def _get_key(self, key_or_type: Union[Type, str]):
        if isinstance(key_or_type, str):
            key = key_or_type
        else:
            keys = [k for k, v in self.types.items() if v == key_or_type]
            if len(keys) == 0:
                raise ValueError('Type `{}` is not registed.'.format(key_or_type))
            key = keys[0]
        return key


common_converter = Converter()
