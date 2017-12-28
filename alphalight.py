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
  textImage = text_to_image('Hello ', '/Library/Fonts/Arial Bold.ttf', 10)
  tw, th = textImage.size
  for i in xrange(tw):
    w, h = (32, 8)  
    image = Image.new('L', (w, h), 1)  
    cropTextImage = textImage.crop((i, 0, tw, th))
    image.paste(cropTextImage, (0,0)) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    s = ScreenSimulator(32, 8)
    for a in arr:
      for b in a:
        s.push(b)
    s.display()
    time.sleep(.1)

for i in xrange(10):
  test()
