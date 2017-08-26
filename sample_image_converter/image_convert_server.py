from io import BytesIO
from PIL import Image
import tornado.ioloop
import tornado_instant_webapi

from image_converter import ImageConverter


# encoder
def image_to_binary(image: Image):
    fobj = BytesIO()
    image.save(fobj, "png")
    return fobj.getvalue()


# decoder
def binary_to_image(b: bytes):
    return Image.open(BytesIO(b))


if __name__ == '__main__':
    tornado_instant_webapi.common_converter.register_new_type(
        key='image',
        t=Image.Image,
        encoder=image_to_binary,
        decoder=binary_to_image,
        content_type='image/png',
    )

    app = tornado_instant_webapi.make_application(ImageConverter, debug=True)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
