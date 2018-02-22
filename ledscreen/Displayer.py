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


class ComponentSlider(object):
    def __init__(self, component_manager):
        self.component_manager = component_manager
        self.component_list = []
        self.index = -1
        self.size = 1

    def get_list(self):
        self.component_list = self.component_manager.get_list()
        self.size = len(self.component_list)

    def next(self, direction='r'):
        if direction == 'r':
            self.index += 1
        else:
            self.index -= 1
        self.index %= self.size
        if self.index == 0:
            self.get_list()
        return self.component_list[self.index]


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
            e = self.current.input(key)
            if e is not None:
                self.queue.put(self.current)
                self.current = e
                self.current.input_in()
        elif key == g.Key.OUT:
            if not self.queue.empty():
                self.current.input_out()
                self.current = self.queue.get()
        elif key == g.Key.PLUS:
            self.current.input(key)
        elif key == g.Key.MINUS:
            self.current.input(key)
        elif key == g.Key.QUIT:
            if self.queue.empty():
                self.current.input(key)


class PlayController(th.Thread):
    def __init__(self, component_slider, displayer, key_reader, stopper=th.Event()):
        super().__init__()
        self.daemon = True
        self.component_slider = component_slider
        self.displayer = displayer
        self.stopper = stopper
        self.component = None
        self.input_manager = InputManager(key_reader, self)
        self.component_changed = False

    def stop(self):
        self.stopper.set()

    def input_in():
        pass
    
    def input_out():
        pass
        
    def input(self, key):
        if self.component:
            if key in [g.Key.PLUS, g.Key.MINUS]:
                previous_component = self.component
                self.component = self.component_slider.next(
                    'r' if key == g.Key.PLUS else '')
                self.component_changed |= self.component != previous_component
            elif key == g.Key.QUIT:
                self.stop()
            elif key == g.Key.IN:
                if self.component.is_editable():
                    return self.component
                else:
                    return None

    def compute_state(self):
        if self.input_manager.current != self:
            return
        if self.component is None:
            self.component = self.component_slider.next()
            self.component_changed = True
        else:
            if self.component.is_enough_displayed():
                previous_component = self.component
                self.component = self.component_slider.next()
                self.component_changed |= self.component != previous_component

    def run(self):
        while not self.stopper.wait(COMPONENT_COMPUTE_RATE):
            self.component_changed = False
            self.compute_state()
            self.input_manager.process()
            self.component.compute_ui(self.displayer, self.component_changed)
