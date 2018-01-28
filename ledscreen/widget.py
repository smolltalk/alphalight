import numpy
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import platform

from ledscreen import utils

class Widget(object):
  def is_animated(self):
    return False

  def display(self, screenImage):
    pass

class StaticImageWidget(Widget):
  def __init__(self, image, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.image = image
    self.tw, self.th = self.image.size

  def display(self, screenImage):
    cropx = 0
    cropy = 0
    cropx2 = min(cropx + self.w, self.tw)
    cropy2 = min(cropy + self.h, self.th)
    cropTextImage = self.image.crop((cropx, cropy, cropx2, cropy2))
    screenImage.paste(cropTextImage, (self.x, self.y)) 
  
class ScrollingImageWidget(Widget):
  
  def __init__(self, image, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.scrollOffset = 0
    tw, th = image.size    
    self.scrollingImage = Image.new('L', (tw + w , th), 1)
    self.scrollingImage.paste(image, (0, 0))
    self.scrollingImage.paste(image, (tw, 0))
    self.tw, self.th = self.scrollingImage.size

  def is_animated(self):
    return True

  def display(self, screenImage):
    cropx = self.scrollOffset
    cropy = 0
    cropx2 = min(cropx + self.w, self.tw)
    cropy2 = min(cropy + self.h, self.th)
    cropTextImage = self.scrollingImage.crop((cropx, cropy, cropx2, cropy2))
    screenImage.paste(cropTextImage, (self.x, self.y)) 
    
    self.scrollOffset += 1
    self.scrollOffset %= self.tw - self.w

class AdaptativeImageWidget(Widget):
  def __init__(self, image, x, y, w, h):
    tw, th = image.size
    if tw < w:
      self.widget = StaticImageWidget(image, x, y, w, h)
    else:
      self.widget = ScrollingImageWidget(image, x, y, w, h)    

  def is_animated(self):
    return self.widget.is_animated()

  def display(self, screenImage):
    self.widget.display(screenImage)
  
class AdaptativeTextWidget(Widget):
  def __init__(self, text, x, y, w, h):
    if platform.system() == 'Darwin':
      textImage = utils.text_to_image(text, '/Library/Fonts/MEMORIA_.ttf', 8)
    else:
      textImage = utils.text_to_image(text, 'c:\\windows\\fonts\\arialbd.ttf', 8)
    tw, th = textImage.size
    if tw < w:
      self.widget = StaticImageWidget(textImage, x, y,w, h)
    else:
      scrollingImage = Image.new('L', (tw + w , th), 1)
      scrollingImage.paste(textImage, (0, 0))
      self.widget = ScrollingImageWidget(scrollingImage, x, y, w, h)    

  def is_animated(self):
    return self.widget.is_animated()
  
  def display(self, screenImage):
    self.widget.display(screenImage)
