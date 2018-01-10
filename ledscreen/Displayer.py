import time
import PIL
import numpy as np
import threading as th

class Displayer(th.Thread):
  def __init__(self, screen, stopper=th.Event()):
    self.screen = screen
    self.componentList = []
    self.stopper = stopper
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

  def stop(self):
    self.stopper.set()

  def run(self):
    while not self.stopper.wait(.1):
      self.display()

def new(screen):
    return Displayer(screen)