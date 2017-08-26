from itertools import chain
import re


def _parse(string):
    """
    >>> _parse('snake_case')
    ('snake', 'case')
    >>> _parse('PascalCase')
    ('pascal', 'case')
    >>> _parse('camelCase')
    ('camel', 'case')
    >>> _parse('HTTPResponseCodeXYZ')
    ('http', 'response', 'code', 'xyz')
    """
    parts = [string]
    parts = tuple(chain.from_iterable(s.split() for s in parts))
    parts = chain.from_iterable(s.split('-') for s in parts)
    parts = chain.from_iterable(s.split('_') for s in parts)
    parts = chain.from_iterable(re.split('([A-Z][a-z]+)', s) for s in parts)
    parts = filter(lambda s: len(s) > 0, parts)
    parts = map(str.lower, parts)
    return tuple(parts)


def _concat(parts, case):
    """
    >>> parts = ('hello', 'world')
    >>> _concat(parts, case='snake')
    'hello_world'
    >>> _concat(parts, case='camel')
    'helloWorld'
    >>> _concat(parts, case='pascal')
    'HelloWorld'
    >>> _concat(parts, case='kebab')
    'hello-world'
    """
    case = case.lower()
    if not case in ('snake', 'camel', 'pascal', 'kebab'):
        raise ValueError(case)

    if case == 'snake':
        return '_'.join(parts)

    if case == 'camel':
        return parts[0] + ''.join(s.title() for s in parts[1:])

    if case == 'pascal':
        return ''.join(s.title() for s in parts)

    if case == 'kebab':
        return '-'.join(parts)


def change_case(string, case):
    return _concat(_parse(string), case)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
