import time
import PIL
import numpy as np
import threading as th

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


class PlayController(th.Thread):
    def __init__(self, component_slider, displayer, stopper=th.Event()):
        super().__init__()
        self.daemon = True
        self.component_slider = component_slider
        self.displayer = displayer
        self.stopper = stopper
        self.component = None

    def stop(self):
        self.stopper.set()

    def compute_state(self):
        if self.component is None:
            self.component = self.component_slider.next()
            return True
        else:
            # TODO Check component.has_terminated
            # TODO Check component has changed
            return False


    def run(self):
        while not self.stopper.wait(COMPONENT_COMPUTE_RATE):
            has_changed = self.compute_state()
            self.component.compute_ui(self.displayer, has_changed)

