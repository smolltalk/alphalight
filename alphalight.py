import time
import PIL
import numpy as np
import threading as th
from ledscreen import components
from ledscreen import ScreenSimulator


# See https://stackoverflow.com/questions/36384353/generate-pixel-matrices-from-characters-in-string
# TODO Autoscroll auto center text component
# TODO Time component
# TODO Weather component
# TODO Manage fonts path in config file
# TODO Clock Alarm
# TODO 
# TODO Add a sequencer
# TODO Manage RGBA colors

class Displayer(th.Thread):
  def __init__(self, screen):
    self.screen = screen
    self.componentList = []

  def addComponent(self, component):
    self.componentList += component
  
  def run(self):
    w, h = screen.size()
    image = PIL.Image.new('L', (w, h), 1)

    for component in self.componentList:
      component.display(image)

    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    for a in arr:
      for b in a:
        self.screen.push(b)
    self.screen.display()

def test():
  screen = ScreenSimulator.new(32, 8)
  d = Displayer(screen)

  scrollingText = components.AdaptativeTextComponent('Hello!', 0, 0, 32, 8)  
  d.addComponent(scrollingText)

  d.start()

test()
