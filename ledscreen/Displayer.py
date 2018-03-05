import time
import PIL
import numpy as np
import threading as th
from ledscreen import getch as g
import queue as q

COMPONENT_COMPUTE_RATE = .1


#
#
# Règles
# - Le composant a une fonction draw qui renvoie une image
# - C'est le composant supérieur qui dessine les composants enfants XYHW
#   en appelant la fonction draw de ses enfants
# - Le cache d'image est à la charge du composant
# - Les coordonnées sont relatifs au parent

# component.draw()
# 	// En fonction de w et h
# 	return


#  - #0 : component.compute(displayer, refresh)

#           displayer.draw()
#
# Question : détecter qu'il n'y a rien à faire

class Displayer(object):
    def __init__(self, screen):
        self.screen = screen

    def display(self, widget):
        w, h = self.screen.size()
        image = PIL.Image.new('L', (w, h), 1)

        image.paste(widget.draw(), widget.coords)

        arr = np.asarray(image)
        arr = np.where(arr, 0, 1)

        for a in arr:
            for b in a:
                self.screen.push(b)
        self.screen.display()


class InputManager(object):

    def __init__(self, key_reader, root):
        self.queue = q.LifoQueue()
        self.current = root
        self.key_reader = key_reader

    def process(self):
        key = self.key_reader.read_key()
        if key == g.Key.IN:
            e = self.current.input({'type': 'key', 'key': key})
            if e is not None:
                self.current.input({'type': 'focus_lost'})
                self.queue.put(self.current)
                self.current = e
                self.current.input({'type': 'focus_in'})
        elif key == g.Key.OUT:
            if not self.queue.empty():
                self.current.input({'type': 'focus_out'})
                self.current = self.queue.get()
                self.current.input({'type': 'focus_back'})
        elif key == g.Key.PLUS:
            self.current.input({'type': 'key', 'key': key})
        elif key == g.Key.MINUS:
            self.current.input({'type': 'key', 'key': key})
        elif key == g.Key.QUIT:
            if self.queue.empty():
                self.current.input({'type': 'key', 'key': key})


class PlayController(th.Thread):
    def __init__(self, slider, displayer, key_reader, stopper=th.Event()):
        super().__init__()
        self.daemon = True
        self.slider = slider
        self.displayer = displayer
        self.stopper = stopper
        self.input_manager = InputManager(key_reader, slider)

    def stop(self):
        self.stopper.set()

    def run(self):
        while not self.stopper.wait(COMPONENT_COMPUTE_RATE):
            self.input_manager.process()
            self.slider.compute_ui(self.displayer, True)
