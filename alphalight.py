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



def test():
  screen = ScreenSimulator.new(32, 8)
  d = Displayer.new(screen)

  scrollingText = components.AdaptativeTextComponent('Hello everybody!', 0, 0, 32, 8)  
  d.addComponent(scrollingText)

  d.daemon = True
  d.start()
  d.join(99999)

test()
