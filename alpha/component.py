from ledscreen import *
from enum import Enum, auto


class AlphaComponent():
    def compute(self):
        pass

    def display(self, screen, data):
        pass


class TimeAlphaComponent(AlphaComponent):
    def compute(self):
        pass

    def display(self, screen, data):
        # components.AdaptativeTextComponent('Hello everybody!', 0, 0, 32, 8)
        widget.AdaptativeTextComponent('Hello everybody!', 0, 0, 32, 8) # I see the risk of malicious code injection


class ComponentManager():

    component_list = []

    def get_list():
        return [self]+self:component_list

    def load(self):
        with open('./conf/components.conf') as f:
            lines = f.readlines()
        for line in lines:
            c = eval(line)
            self.component_list.append(c)

    def compute(self):
        load()

class ComponentComputer():

    def __init__(self, component_manager):
        self.component_manager = component_manager
        self.component_iter = iter([])
        th.Thread.__init__(self)

    def stop(self):
        self.stopper.set()

    def compute(self):
        try:
            c = next(self.component_iter)
        except StopIteration:
            c = None
            self.component_iter = iter(self.component_manager.get_list())
        
        if c:
            c.compute()

    def run(self):
        while not self.stopper.wait(.01):
            self.compute()
