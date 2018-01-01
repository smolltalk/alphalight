from __future__ import print_function
import sys
import random
import numpy
import PIL
import os
import ctypes
import time
import string

import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

# See https://stackoverflow.com/questions/36384353/generate-pixel-matrices-from-characters-in-string

class ScreenSimulator:

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.buffer = [0] * w * h
    
  def push(self, v):
    self.buffer = [v] + self.buffer[:-1]
    
  def display(self):
    sys.stdout.write("\033[1;31m")
    i = self.w * self.h - 1
    for y in xrange(self.h):
      for x in xrange(self.w):
        if self.buffer[i] == 1: 
          sys.stdout.write(u'\u25cf ')
        else:
          sys.stdout.write('  ')
        i = i - 1
      print("")
    sys.stdout.write("\033[8A")
    sys.stdout.write("\033[64D")
 
class ScrollingImage:
  
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
    screenImage.paste(cropTextImage, (0, 0)) 
    
    self.scrollOffset += 1
    self.scrollOffset %= self.tw - self.w
    
def text_to_image(text, fontpath, fontsize):
    font = ImageFont.truetype(fontpath, fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = np.asarray(image)
    arr = arr[(arr != 1).any(axis=1)]
    result = Image.fromarray(arr)
    return result

def test():
  w, h = (32, 8)  

  textImage = text_to_image('Bonjour Elena et Jules !', '/Library/Fonts/Arial Bold.ttf', 10)
  tw, th = textImage.size
  scrollingImage = Image.new('L', (tw + w , th), 1)
  scrollingImage.paste(textImage, (0, 0))

  scrollingText = ScrollingImage(scrollingImage, 0, 0, 32, 8)  
  
  while True:
    image = Image.new('L', (w, h), 1) 
    scrollingText.display(image) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    s = ScreenSimulator(32, 8)
    for a in arr:
      for b in a:
        s.push(b)
    s.display()
    time.sleep(.1)

test()
