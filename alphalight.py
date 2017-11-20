import sys

class ScreenSimulator:

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.buffer = [0] * w * h
    
  def push(self, v):
    self.buffer = [v] + self.buffer[::-1]
    
  def display(self):
    sys.stdout.write("\033[2J")
    i = 0
    for y in xrange(self.h):
      for x in xrange(self.w):
        if self.buffer[i] == 1: 
          sys.stdout.write("X")
        else:
          sys.stdout.write(".")
        i = i + 1
      print("")

s = ScreenSimulator(32, 8)
s.push(1)
s.push(1)
s.push(1)
s.push(1)
s.push(1)

s.display()

