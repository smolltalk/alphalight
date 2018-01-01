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
from ledscreen import ScreenSimulator
from ledscreen import utils
from ledscreen import components

# See https://stackoverflow.com/questions/36384353/generate-pixel-matrices-from-characters-in-string
# TODO Autoscroll auto center text component
# TODO Time component
  
def test():
  w, h = (32, 8)  

  scrollingText = components.AdaptativeTextComponent('Bonjour Elena et Jules !', 0, 0, 32, 8)  
  s = ScreenSimulator.new(32, 8)
  
  while True:
    image = Image.new('L', (w, h), 1) 
    scrollingText.display(image) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    for a in arr:
      for b in a:
        s.push(b)
    s.display()
    time.sleep(.1)

test()
