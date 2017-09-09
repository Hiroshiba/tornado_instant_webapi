# Image Converter

This is the sample project to use `tornado_instant_webapi`.

Please see [Jupyter notebook file](./readme.ipynb).

## Run server

Firstly, run `image_convert_server.py` like this:
```bash
pip install -r requirements.txt
python image_convert_server.py
```

## Request

Then, you can request to `http://localhost:8000/`.

## Code detail

In this project, `ImageConverter` class was defined like [this](./readme.ipynb).

```python
class ImageConverter(object):
    ...
    @staticmethod
    def width(image: Image):
        return image.width

    @staticmethod
    def height(image: Image):
        return image.height

    @staticmethod
    def convert(image: Image, mode: str = None, matrix=None, dither: int = None, palette: int = 0, colors: int = 256):
        return image.convert(mode, matrix, dither, palette, colors)
    ...
```

And make `Tornado` application with `ImageConverter` class.

```python
app = tornado_instant_webapi.make_application(ImageConverter, debug=True)
```

Then, `tornado_instant_webapi` library scan the method or module or class or value, and make `Tornado` handlers with automatically.

You can request to `/width` or `/height` or `/convert`, defined methods under `ImageConverter` class.
