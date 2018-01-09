import time
import PIL
import numpy as np
import threading as th

class Displayer(th.Thread):
  def __init__(self, screen):
    self.screen = screen
    self.componentList = []
    th.Thread.__init__(self)

  def addComponent(self, component):
    self.componentList.append(component)

  def display(self):
    w, h = self.screen.size()
    image = PIL.Image.new('L', (w, h), 1)

    for component in self.componentList:
      component.display(image)

    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    
    for a in arr:
      for b in a:
        self.screen.push(b)
    self.screen.display()

  def run(self):
    while True:
      self.display()
      time.sleep(.1)

def new(screen):
    return Displayer(screen)