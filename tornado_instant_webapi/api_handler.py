from collections import ChainMap
import tornado.web
import typing

from tornado_instant_webapi.converter import common_converter

QueryTypes = typing.Dict[str, typing.Type]
OutputType = typing.Type


class InstantApiHandler(tornado.web.RequestHandler):
    def __init__(
            self,
            *args,
            methods: typing.List[str],
            query_types: QueryTypes,
            output_type: OutputType,
            process: typing.Callable,
            instance=None,
            converter=common_converter,
            **kwargs
    ):
        """
        Generate Tornado handler from input/output types.
        :param args: RequestHandler's args
        :param methods: Methods for this handler. 'all', 'get', 'post' are allowed.
        :param query_types: Types of input values.
        :param output_type: Type of return value.
        :param process: Process for making return value.
        :param instance: This value is used first argument (when process is instance method, this value is needed).
        :param converter: Converter the Python object and the request parameter, each other.
        :param kwargs: RequestHandler's kwargs
        """
        super().__init__(*args, **kwargs)
        methods = [s.lower() for s in methods]
        if 'all' in methods:
            methods.append('get')
            methods.append('post')

        self.methods = methods
        self.query_types = query_types
        self.output_type = output_type
        self.process = process
        self.instance = instance
        self.converter = converter

    def initialize(self, **kwargs):  # wrap RequestHandler's method
        self.keywords = kwargs

    @property
    def queries(self):
        """
        Return request arguments and files.
        """
        return ChainMap(
            {k: self.get_argument(k) for k in self.request.arguments.keys()},
            {k: vs[0]['body'] for k, vs in self.request.files.items()},
        )

    @staticmethod
    def call_function(func: typing.Callable, instance: typing.Optional, arguments: typing.Mapping[str, any]):
        """
        Call process function with/without instance.
        When func is the instance method, the value of instance must be needed.
        """
        if instance is None:
            obj = func(**arguments)
        else:
            obj = func(instance, **arguments)
        return obj

    def run_process(
            self,
            query_types: QueryTypes,
            output_type: OutputType,
            process: typing.Callable,
    ):
        """
        Run process.
        Encode params -> Join keywords -> Call Process -> Decode object -> Return
        """
        queries = {key: self.converter.decode(value, query_types[key]) for key, value in self.queries.items()}
        kwargs = ChainMap(self.keywords, queries)
        obj = self.call_function(process, self.instance, kwargs)
        obj = self.converter.encode(obj, output_type)
        self.write(obj)

    def get(self):  # wrap RequestHandler's method
        if 'get' in self.methods:
            self._fire()
        else:
            super().get()

    def post(self):  # wrap RequestHandler's method
        if 'post' in self.methods:
            self._fire()
        else:
            super().get()

    def _fire(self):
        self.run_process(
            query_types=self.query_types,
            output_type=self.output_type,
            process=self.process,
        )
