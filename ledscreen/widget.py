import numpy
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
from sys import platform

from ledscreen import utils


class Widget(object):
    # TODO: blink

    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def coords(self):
        return (self.x, self.y)

    def is_animation_end(self):
        return True


class StaticImage(Widget):
    def __init__(self, image, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image = image
        self.tw, self.th = self.image.size

    def draw(self):
        cropx = 0
        cropy = 0
        cropx2 = min(cropx + self.w, self.tw)
        cropy2 = min(cropy + self.h, self.th)
        crop_text_image = self.image.crop((cropx, cropy, cropx2, cropy2))
        return crop_text_image


class ScrollingImage(Widget):

    def __init__(self, image, x, y, w, h):
        super().__init__(x, y, w, h)
        self.scroll_offset = 0
        tw, th = image.size
        self.scrolling_image = Image.new('L', (tw + w, th), 1)
        self.scrolling_image.paste(image, (0, 0))
        self.scrolling_image.paste(image, (tw, 0))
        self.tw, self.th = self.scrolling_image.size
        self.scrolling_size = self.tw - self.w

    def draw(self):
        cropx = self.scroll_offset
        cropy = 0
        cropx2 = min(cropx + self.w, self.tw)
        cropy2 = min(cropy + self.h, self.th)
        crop_text_image = self.scrolling_image.crop(
            (cropx, cropy, cropx2, cropy2))
        self.scroll_offset += 1
        self.scroll_offset %= self.scrolling_size
        return crop_text_image

    def is_animation_end(self):
        return self.scroll_offset == self.scrolling_size - self.w


class AdaptativeImage(Widget):
    def __init__(self, image, x, y, w, h):
        super().__init__(x, y, w, h)
        tw, th = image.size
        if tw < w:
            self.image = StaticImage(image, x, y, w, h)
        else:
            self.image = ScrollingImage(image, x, y, w, h)

    def draw(self):
        return self.image.draw()


PLATFORM_FONT_DIR = {'win32': 'c:\\windows\\fonts\\',
                     'darwin': '/Library/Fonts/', 'linux': '', 'linux2': ''}


class AdaptativeText(Widget):
    def __init__(self, text, x, y, w, h, font_name='PressStart2P-Regular', font_size=8, font_dir=None):
        super().__init__(x, y, w, h)
        # http://www.fontsc.com/font/category/pixel-bitmap/8px?page=2
        # text_image = utils.text_to_image(text, '/Library/Fonts/Arial Bold.ttf', 10)
        # arialbd.ttf', 10)
        # Good for text shift: PressStart2P-Regular.ttf', 8)
        # Memoria.ttf', 7)
        # MiniTot.ttf', 8)
        # type_writer.ttf', 8)
        # teacp__.ttf', 7)
        # Good for number : Fleftex_M.ttf', 8) Emulator.ttf', 8)
        # pixearg.ttf', 8) pixeab_.ttf', 8)
        # fixed_bo.ttf', 6)
        # fixed_v0.ttf', 4) 02
        # fixed_v0_0.ttf', 8) 01
        # serif_v0.ttf', 6)
        # swf!t__.ttf', 8)

        if not font_dir:
            self.font_dir = PLATFORM_FONT_DIR[platform]
        self.font_name = font_name
        self.font_size = font_size
        self.text = text

    def compute_image(self):
        text_image = utils.text_to_image(
            _text, self.font_dir + self.font_name + '.ttf', self.font_size)

        tw, th = text_image.size
        if tw < w:
            self.image = StaticImage(text_image, x, y, w, h)
        else:
            scrolling_image = Image.new('L', (tw + w, th), 1)
            scrolling_image.paste(text_image, (0, 0))
            self.image = ScrollingImage(scrolling_image, x, y, w, h)

    @property
    def text(self):
        return _text

    @text.setter
    def text(self, val)
        _text = val
        self.compute_image()

    def draw(self):
        return self.image.draw()

    def is_animation_end(self):
        return self.image.is_animation_end()


class AdaptativeNumeric(Widget):
    __init__(self, value=value_min, value_min, value_max, x, y, w, h, font_name='Fleftex_M', font_size=8, font_dir=None):
        super().__init__(x, y, w, h)
        self.value_min = value_min
        self.value_max = value_max
        self.text_component = AdaptativeText(
            '', x, y, w, h, font_name, font_size, font_dir)
        self.value = value

    @property
    def value(self):
        return _text

    @text.setter
    def value(self, val)
        if val < value_min:
            raise Exception(
                'Value ({}) is less than min ({})'.format(val, value_min))
        if val > value_max:
            raise Exception(
                'Value ({}) is greater than min ({})'.format(val, value_min))

        _value = val
        self.text_component.text = str(_value)

    def draw(self):
        return self.text_component.draw()

    def is_animation_end(self):
        return self.text_component.is_animation_end()
