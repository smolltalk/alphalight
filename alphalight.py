import time
import PIL
import numpy as np
from ledscreen import components
from ledscreen import ScreenSimulator

# See https://stackoverflow.com/questions/36384353/generate-pixel-matrices-from-characters-in-string
# TODO Autoscroll auto center text component
# TODO Time component
# TODO Weather component
# TODO Manage fonts path in config file

def test():
  w, h = (32, 8)  

  scrollingText = components.AdaptativeTextComponent('Hello!', 0, 0, 32, 8)  
  s = ScreenSimulator.new(32, 8)
  
  while True:
    image = PIL.Image.new('L', (w, h), 1) 
    scrollingText.display(image) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    for a in arr:
      for b in a:
        s.push(b)
    s.display()
    time.sleep(.1)

test()
