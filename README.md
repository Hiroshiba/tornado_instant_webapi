# Tornado Instant WebAPI  [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](./LICENSE)

This is a library for automatically generating [Tornado](http://www.tornadoweb.org/) web API server from Python object with [Type Hints](https://www.python.org/dev/peps/pep-0484/).

## Installation

```bash
pip install git+https://github.com/Hiroshiba/tornado_instant_webapi
```

## Usage

You can make web API from Python object: Classes, Modules, Dicts, Objects. 

This is an example of starting API server from a class.

```python
import tornado.ioloop
from tornado_instant_webapi import make_application

class Calculator(object):
    @staticmethod
    def double(number: float) -> float:
        return 2 * number

if __name__ == '__main__':
    app = make_application(Calculator)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
```

Then, you can call API:
```bash
$ curl http://localhost:8000/double?number=100
200.0
```


### Original type parameter
You can use an original type easily, by adding the encoder or decoder.

This is the example for using [NumPy](http://www.numpy.org/).
```python
import tornado.ioloop
from tornado_instant_webapi import common_converter, make_application

import json
import numpy

class NumpyCalculator(object):
    @staticmethod
    def sum(array: numpy.ndarray) -> float:
        return array.sum()

def nparray_decoder(s: str):
    return numpy.asarray(json.loads(s))

if __name__ == '__main__':
    common_converter.register_new_type(
        key='nparray',
        t=numpy.ndarray,
        decoder=nparray_decoder,
    )

    app = make_application(NumpyCalculator)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
```

Then, you can call API:
```bash
$ curl --globoff http://localhost:8000/sum?array=[1,2,3]
6
```

### Nested object

This library can make web API from nested Python object.

```python
if __name__ == '__main__':
    nested = {
        'Calculator': Calculator,
        'NumpyCalculator': NumpyCalculator,
    }
    app = make_application(nested, string_case='snake')
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
```

Then, you can call API:
```bash
$ curl http://localhost:8000/calculator/double?number=100
200.0

$ curl --globoff http://localhost:8000/numpy_calculator/sum?array=[1,2,3]
6
```

## Sample Code
[Image Converter](./sample_image_converter) is the sample web API server for the image convert.

## License
MIT License, see [LICENSE](./LICENSE).
