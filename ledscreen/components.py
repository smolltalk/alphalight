import numpy
import PIL

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

from ledscreen import utils

class StaticImageComponent:
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
  
class ScrollingImageComponent:
  
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

  def display(self, screenImage):
    cropx = self.scrollOffset
    cropy = 0
    cropx2 = min(cropx + self.w, self.tw)
    cropy2 = min(cropy + self.h, self.th)
    cropTextImage = self.scrollingImage.crop((cropx, cropy, cropx2, cropy2))
    screenImage.paste(cropTextImage, (self.x, self.y)) 
    
    self.scrollOffset += 1
    self.scrollOffset %= self.tw - self.w

class AdaptativeImageComponent:
  def __init__(self, image, x, y, w, h):
    tw, th = image.size
    if tw < w:
      self.component = StaticImageComponent(image, x, y, w, h)
    else:
      self.component = ScrollingImageComponent(image, x, y, w, h)    

  def display(self, screenImage):
    self.component.display(screenImage)
  
class AdaptativeTextComponent:
  def __init__(self, text, x, y, w, h):
    #textImage = utils.text_to_image(text, '/Library/Fonts/Arial Bold.ttf', 10)
    textImage = utils.text_to_image(text, 'c:\\windows\\fonts\\arialbd.ttf', 10)
    tw, th = textImage.size
    if tw < w:
      self.component = StaticImageComponent(textImage, x, y,w, h)
    else:
      scrollingImage = Image.new('L', (tw + w , th), 1)
      scrollingImage.paste(textImage, (0, 0))
      self.component = ScrollingImageComponent(scrollingImage, x, y, w, h)    

  def display(self, screenImage):
    self.component.display(screenImage)
