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

# Mode non superposé #1
#  - Pas de besoin de stocker l'image précédente
#  - C'est le composant qui décide de se rafraichir ou pas
#  - Seul le flag refresh peut demander au composant de se refraichir
#  - Pas de notion de composition à différent niveau de refresh


#  - #0 : component.compute(displayer, refresh)

#           displayer.draw()
#
# Question : détecter qu'il n'y a rien à faire


class ComponentSlider(object):
    def __init__(self, component_manager):
        self.component_manager = component_manager
        self.component_list = []
        self.index = -1

    def get_list(self):
        self.component_list = self.component_manager.get_list()

    def next(self, direction='r'):
        if direction == 'r':
            self.index += 1
        else:
            self.index -= 1
        self.index %= size(self.component_list)
        return self.component_list[self.index]


class PlayController(th.Thread):
    def __init__(self, component_slider, stopper=th.Event()):
        self.component_slider = component_slider
        self.stopper = stopper
        self.component = None

    def stop(self):
        self.stopper.set()

    def compute_state(self):
        if self.component is None:
            self.component = self.component_slider.next()
        else:

    def run(self):
        while not self.stopper.wait(COMPONENT_COMPUTE_RATE):
            has_changed = self.compute_state()
            self.component.compute(self.displayer, has_changed)


class Displayer(object):
    def __init__(self, screen):
        self.screen = screen

    def display(self, component):
        self.component_list = self.component_manager.get_list()

        w, h = self.screen.size()
        image = PIL.Image.new('L', (w, h), 1)

        component.display(image, None)

        arr = np.asarray(image)
        arr = np.where(arr, 0, 1)

        for a in arr:
            for b in a:
                self.screen.push(b)
        self.screen.display()
