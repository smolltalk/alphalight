import time
import PIL
import numpy as np
import threading as th
from ledscreen import components
from ledscreen import ScreenSimulator
from ledscreen import Displayer

# See https://stackoverflow.com/questions/36384353/generate-pixel-matrices-from-characters-in-string
# TODO Autoscroll auto center text component
# TODO Time component
# TODO Weather component
# TODO Manage fonts path in config file
# TODO Clock Alarm
# TODO 
# TODO Add a sequencer
# TODO Manage RGBA colors
# TODO Type controller enter/exit/+/-

# Rules
# 1: List of Widget
# 2: For each widget, maybe something to do in backend
# 3: 
# 4: Configuration mode is the highest graphic priority
# 5: Notifications preempt

class ComponentManager():
  
  componentList = []

  def load(self):
    with open('./conf/components.conf') as f:
      lines = f.readlines()
    for line in lines:
      c = eval(line)
      self.componentList.append(c)   

# Component Manager
cm = ComponentManager()
cm.load()

# Screen
screen = ScreenSimulator.new(32, 8)

# Displayer
d = Displayer.new(screen)

for c in cm.componentList:
  d.addComponent(c)

d.start()

end = False
while not end:
  v = input()
  end = True

d.stop()
