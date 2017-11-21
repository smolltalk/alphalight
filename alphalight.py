import sys
import random

class ScreenSimulator:

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.buffer = [0] * w * h
    
  def push(self, v):
    self.buffer = [v] + self.buffer[:-1]
    
  def display(self):
    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[1;31m")
    i = self.w * self.h - 1
    for y in xrange(self.h):
      for x in xrange(self.w):
        if self.buffer[i] == 1: 
          sys.stdout.write(u'\u25cf ')
        else:
          sys.stdout.write(u'  ')
        i = i - 1
      print("")

      
s = ScreenSimulator(32, 8)
for i in xrange(32*8):
  s.push(random.randint(0, 1))
s.display()

