import time
import PIL
import numpy as np
import threading as th


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
        while not self.stopper.wait(.1):
            has_changed = self.compute_state()
            self.component.compute_ui(
                self.input_reader, self.displayer, self.sound_player, has_changed)


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
