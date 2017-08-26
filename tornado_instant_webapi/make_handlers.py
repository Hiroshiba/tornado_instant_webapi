from collections import ChainMap
import inspect
from typing import Dict, Tuple, Type

from tornado_instant_webapi.change_case import change_case
from tornado_instant_webapi.converter import common_converter
from tornado_instant_webapi.api_handler import QueryTypes, OutputType
from tornado_instant_webapi.api_handler import InstantApiHandler


def _through_pass(obj):
    return obj


def _get_args_types(method) -> (QueryTypes, OutputType):
    """
    >>> def func(arg1: int, arg2: str) -> float: ...
    >>> _get_args_types(func) == (dict(arg1=int, arg2=str), float)
    True
    """
    type_dict = inspect.getfullargspec(method).annotations  # type: Dict[str, Type]
    output_type = type_dict.pop('return', None)
    query_types = type_dict
    return query_types, output_type


def _get_members(obj):
    """
    >>> class Class:
    ...     def method1(self): ...
    ...     def method2(self): ...
    >>> names, funcs = zip(*_get_members(Class))
    >>> names == ('method1', 'method2')
    True
    """
    if isinstance(obj, dict):
        members = obj.items()
    else:
        members = inspect.getmembers(obj)

    return [
        (member_name, member)
        for member_name, member in members
        if member_name[0] != '_'  # remove private member
    ]


def _handler_name(keys: Tuple[str, ...], string_case='snake'):
    """
    >>> _handler_name(('a', 'b', 'c'))
    '/a/b/c'
    """
    return '/' + '/'.join(change_case(key, string_case) for key in keys)


def _make_arguments_recursive(obj, keys: Tuple[str, ...]) -> Dict[Tuple[str], Dict]:
    arguments = {}  # type: Dict[Tuple[str], Dict]

    for member_name, member in _get_members(obj):
        new_keys = keys + (member_name,)

        # recursive
        need_recursive = \
            inspect.isclass(member) or \
            isinstance(member, dict) or \
            (
                not inspect.ismodule(member) and
                not inspect.isbuiltin(member) and
                not isinstance(member, (int, float, str, bytes, list))
            )
        if need_recursive:
            arguments = ChainMap(arguments, _make_arguments_recursive(member, new_keys))

        # make arguments
        query_types, output_type = _get_args_types(member)

        if not callable(member):
            kwargs = dict(
                query_types={},
                output_type=type(member),
                process=_through_pass,
                instance=member,
            )
        elif inspect.ismethod(member):  # instance method
            kwargs = dict(
                query_types=query_types,
                output_type=output_type,
                process=getattr(obj.__class__, member_name),
                instance=obj,
            )
        else:  # global function
            kwargs = dict(
                query_types=query_types,
                output_type=output_type,
                process=member,
            )

        arguments[new_keys] = kwargs

    return arguments


def make_handlers(obj, converter=common_converter, methods=None, string_case='snake'):
    """
    Make Tornado Application handlers from Python objects.
    :param obj: Python object: Classes, Modules, Dicts, Objects.
    :param converter: Converter the Python object and the request parameter, each other.
    :param methods: Methods for this handler. 'all', 'get', 'post' are allowed.
    :param string_case: Case of path strings.
    :return: Tornado Application handlers. List of (path, HandlerClass, arguments).
    """
    if methods is None:
        methods = ['all']

    arguments = _make_arguments_recursive(obj, ())
    handlers = []
    for handler_keys, kwargs in arguments.items():
        handler_name = _handler_name(handler_keys, string_case=string_case)
        kwargs = ChainMap(kwargs, dict(methods=methods, converter=converter))
        handlers.append((handler_name, InstantApiHandler, kwargs))

    return handlers
