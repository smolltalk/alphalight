import sys
import random
import numpy
import PIL
import os
import ctypes

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
    #os.system('cls')
    i = self.w * self.h - 1
    for y in xrange(self.h):
      for x in xrange(self.w):
        if self.buffer[i] == 1: 
          #sys.stdout.write(u'\u25cf ')
          sys.stdout.write('\xfe  ')
        else:
          sys.stdout.write('   ')
        i = i - 1
      print("")


kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

s = ScreenSimulator(32, 8)
for i in xrange(32*8):
  s.push(random.randint(0, 1))
s.display()

