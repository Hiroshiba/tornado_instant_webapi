from PIL.Image import Image


class ImageConverter(object):
    @staticmethod
    def format(image: Image):
        return image.format

    @staticmethod
    def format_description(image: Image):
        return image.format_description

    @staticmethod
    def im(image: Image):
        return image.im

    @staticmethod
    def mode(image: Image):
        return image.mode

    @staticmethod
    def size(image: Image):
        return image.size

    @staticmethod
    def palette(image: Image):
        return image.palette

    @staticmethod
    def info(image: Image):
        return image.info

    @staticmethod
    def category(image: Image):
        return image.category

    @staticmethod
    def readonly(image: Image):
        return image.readonly

    @staticmethod
    def pyaccess(image: Image):
        return image.pyaccess

    @staticmethod
    def encoderinfo(image: Image):
        return image.encoderinfo

    @staticmethod
    def encoderconfig(image: Image):
        return image.encoderconfig

    @staticmethod
    def width(image: Image):
        return image.width

    @staticmethod
    def height(image: Image):
        return image.height

    @staticmethod
    def convert(image: Image, mode: str = None, matrix=None, dither: int = None, palette: int = 0, colors: int = 256):
        return image.convert(mode, matrix, dither, palette, colors)

    @staticmethod
    def quantize(image: Image, colors: int = 256, method: int = None, kmeans: int = 0, palette=None):
        return image.quantize(colors, method, kmeans, palette)

    @staticmethod
    def copy(image: Image):
        return image.copy()

    @staticmethod
    def crop(image: Image, box: tuple = None):
        return image.crop(box)

    @staticmethod
    def getbands(image: Image):
        return image.getbands()

    @staticmethod
    def getbbox(image: Image):
        return image.getbbox()

    @staticmethod
    def getextrema(image: Image):
        return image.getextrema()

    @staticmethod
    def getpalette(image: Image):
        return image.getpalette()

    @staticmethod
    def getpixel(image: Image, xy: tuple):
        return image.getpixel(xy)

    @staticmethod
    def getprojection(image: Image):
        return image.getprojection()

    @staticmethod
    def histogram(image: Image, mask=None, extrema=None):
        return image.histogram(mask, extrema)

    @staticmethod
    def paste(image: Image, im: Image, box: tuple = None, mask=None):
        return image.paste(im, box, mask)

    @staticmethod
    def alpha_composite(image: Image, im: Image, dest=(0, 0), source=(0, 0)):
        return image.alpha_composite(im, dest, source)

    @staticmethod
    def point(image: Image, lut: list, mode: str = None):
        return image.point(lut, mode)

    @staticmethod
    def resize(image: Image, size: tuple, resample: int = 0):
        return image.resize(size, resample)

    @staticmethod
    def rotate(image: Image, angle: float, resample: int = 0, expand: bool = False, center: tuple = None,
               translate: tuple = None):
        return image.rotate(angle, resample, expand, center, translate)

    @staticmethod
    def split(image: Image, l: int):
        return image.split()[l]

    @staticmethod
    def tell(image: Image):
        return image.tell()

    @staticmethod
    def transform(image: Image, size: tuple, method: int, data=None, resample: int = 0, fill: int = 1):
        return image.transform(size, method, data, resample, fill)

    @staticmethod
    def transpose(image: Image, method: int):
        return image.transpose(method)

    @staticmethod
    def effect_spread(image: Image, distance: int):
        return image.effect_spread(distance)
