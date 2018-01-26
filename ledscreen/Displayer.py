import time
import PIL
import numpy as np
import threading as th

class Displayer(th.Thread):
  def __init__(self, component_manager, screen, stopper=th.Event()):
    self.component_manager = component_manager
    self.screen = screen
    self.component_list = []
    self.stopper = stopper
    th.Thread.__init__(self)

  def display(self):
    self.component_list = self.component_manager.get_list()

    w, h = self.screen.size()
    image = PIL.Image.new('L', (w, h), 1)

    for component in self.component_list:
      component.display(image, None)

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

def new(component_manager, screen):
    return Displayer(component_manager, screen)