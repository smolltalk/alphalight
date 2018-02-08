from ledscreen import *
from enum import Enum, auto
import threading as th
import datetime


class PeriodicTrigger():

    def __init__(self, period, counter=0):
        self.period = period
        self.counter = counter

    def tick(self):
        ret = self.is_triggered()
        self.counter += 1
        return ret

    def is_triggered(self):
        return self.counter % self.period == 0


class AlphaComponent(object):

    def __init__(self):
        self.compute_trigger = PeriodicTrigger(600)
        self.compute_ui_trigger = PeriodicTrigger(1)

    def compute(self):
        if self.compute_trigger.tick():
            self.do_compute()

    def compute_ui(self, displayer, ask_refresh):
        if self.compute_ui_trigger.tick():
            self.do_compute_ui(displayer, ask_refresh)

    def do_compute(self):
        pass

    def do_compute_ui(self, displayer, ask_refresh):
        pass


class TimeAlphaComponent(AlphaComponent):

    def __init__(self):
        super().__init__()
        self.displayable = True
        self.hour = None
        

    def do_compute_ui(self, displayer, ask_refresh):
        hour = datetime.datetime.now().strftime('%H:%M')
        if self.hour != hour:
            self.hour = hour
            self.c = widget.AdaptativeText(hour, 0, 0, 32, 8)

        displayer.display(self.c)


class ComponentManager(AlphaComponent):

    component_list = []

    def get_list(self):
        return self.component_list + [self]

    def load(self):
        with open('./conf/components.conf') as f:
            lines = f.readlines()
        for line in lines:
            c = eval(line)
            self.component_list.append(c)

    def do_compute(self):
        self.load()


class Computer(th.Thread):

    def __init__(self, component_manager, stopper=th.Event()):
        self.component_manager = component_manager
        self.component_iter = iter([])
        self.stopper = stopper
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
