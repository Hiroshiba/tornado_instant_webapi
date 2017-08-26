import tornado.ioloop
import tornado.web

from tornado_instant_webapi.converter import common_converter
from tornado_instant_webapi.make_handlers import make_handlers


def make_application(obj, converter=common_converter, string_case='snake', debug=False, **settings):
    """
    Make Tornado Application from Python objects.
    :param obj: Python object: Classes, Modules, Dicts, Objects.
    :param converter: Converter the Python object and the request parameter, each other.
    :param string_case: Case of path strings.
    :param debug: If True, show generated web APIs.
    :param settings: Settings of Tornado Application.
    :return: Tornado Application.
    """
    handlers = make_handlers(obj, converter=converter, string_case=string_case)

    if debug:
        from pprint import pprint
        d = {name: arguments['process'] for name, _, arguments in handlers}
        pprint(d)

    return tornado.web.Application(handlers, debug=debug, **settings)
