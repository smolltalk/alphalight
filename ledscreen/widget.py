import numpy
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import platform

from ledscreen import utils


class Widget(object):
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


class AdaptativeText(Widget):
    def __init__(self, text, x, y, w, h):
        super().__init__(x, y, w, h)
        text_image = utils.text_to_image(text, '/Library/Fonts/Arial Bold.ttf', 10)
        #text_image = utils.text_to_image(
        #    text, 'c:\\windows\\fonts\\arialbd.ttf', 10)
        tw, th = text_image.size
        if tw < w:
            self.image = StaticImage(text_image, x, y, w, h)
        else:
            scrolling_image = Image.new('L', (tw + w, th), 1)
            scrolling_image.paste(text_image, (0, 0))
            self.image = ScrollingImage(scrolling_image, x, y, w, h)

    def draw(self):
        return self.image.draw()

    def is_animation_end(self):
        return self.image.is_animation_end()
