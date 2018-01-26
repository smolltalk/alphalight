import time
import PIL
import numpy as np
import threading as th
from ledscreen import *
from alpha.component import *

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
# TODO Rename variable to snake_case

# Rules
# 1: List of Widget
# 2: For each widget, maybe something to do in backend
# 3:
# 4: Configuration mode is the highest graphic priority
# 5: Notifications preempt


# Component Manager
cm = ComponentManager()

# Screen
screen = ScreenSimulator.new(32, 8)

# Computer
c = Computer(cm)

# Displayer
d = Displayer.new(cm, screen)

c.start()
d.start()

end = False
while not end:
    v = input()
    end = True

c.stop()
d.stop()
