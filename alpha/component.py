from ledscreen import *
from ledscreen import getch as g
from enum import Enum, auto
from datetime import datetime
import threading as th


class PeriodicTrigger():

    def __init__(self, period, offset=0):
        self.period = period
        self.offset = offset
        self.reset()

    def reset(self):
        self.counter = self.offset

    def tick(self):
        ret = self.is_triggered()
        self.counter += 1
        return ret

    def is_triggered(self):
        return self.counter % self.period == 0


class DurationTrigger():

    def __init__(self, duration_sec):
        self.duration_sec = duration_sec
        self.reset()

    def reset(self):
        self.start_time = datetime.now()

    def is_triggered(self):
        now = datetime.now()
        diff = now - self.start_time
        return diff.total_seconds() > self.duration_sec


class AttributeDict(dict):

    _has_changed = False

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, item):
        _has_changed = True
        super().__setitem__(key, item)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, item):
        self.__setitem__(key, item)

    @property
    def has_changed(self):
        return self._has_changed

    def reset_changed(self):
        _has_changed = False


class AlphaComponent(object):

    def __init__(self, compute_period=600, compute_ui_period=1, display_duration_sec=5):
        self.compute_trigger = PeriodicTrigger(compute_period)
        self.compute_ui_trigger = PeriodicTrigger(compute_ui_period)
        self.display_duration = DurationTrigger(display_duration_sec)
        self._data = None

    @property
    def data(self):
        return self._data

    def compute_data(self):
        if self.compute_trigger.tick():
            data = self.do_compute_data()
            if data:
                self._data = data.copy()

    def compute_ui(self, displayer, ask_refresh):
        if ask_refresh:
            self.compute_ui_trigger.reset()
            self.display_duration.reset()

        if self.compute_ui_trigger.tick():
            self.do_compute_ui(displayer, ask_refresh)

    def is_enough_displayed(self):
        return self.display_duration.is_triggered()

    def is_editable(self):
        return False

    def do_compute(self):
        pass

    def do_compute_ui(self, displayer, ask_refresh):
        pass

    def input(self, key):
        pass


class TimeComponent(AlphaComponent):

    def __init__(self):
        super().__init__()
        self.displayable = True
        self.hour = None

    def do_compute_ui(self, displayer, ask_refresh):
        hour = datetime.now().strftime('%H:%M')
        if self.hour != hour:
            self.hour = hour
            self.c = widget.AdaptativeText(
                hour, 0, 0, 32, 8, font_name='Fleftex_M')

        displayer.display(self.c)


class AlarmComponent(AlphaComponent):
    # TODO blink

    def __init__(self):
        super().__init__()
        self.hours = 0
        self.minutes = 0
        self.data_changed = False
        self.edit_hours = True

    def do_compute_ui(self, displayer, ask_refresh):
        if ask_refresh or self.data_changed:
            c = widget.AdaptativeText('{:2}:{:02d}'.format(
                self.hours, self.minutes), 0, 0, 32, 8, font_name='Fleftex_M')
            self.data_changed = False
            displayer.display(c)

    def is_editable(self):
        return True

    def input(self, key):
        if key == g.Key.PLUS:
            if self.edit_hours:
                self.hours = (self.hours + 1) % 24
            else:
                self.minutes = (self.minutes + 1) % 60
            self.data_changed = True
        elif key == g.Key.MINUS:
            if self.edit_hours:
                self.hours = (self.hours - 1) % 24
            else:
                self.minutes = (self.minutes - 1) % 60
            self.data_changed = True
        elif key == g.Key.IN:
            self.edit_hours = not self.edit_hours
            self.data_changed = True


class ComponentManager(AlphaComponent):

    component_list = []

    def get_list(self):
        return self.component_list + [self]

    def load(self):
        self.component_list = []
        with open('./conf/components.conf') as f:
            lines = f.readlines()
        for line in lines:
            c = eval(line)
            self.component_list.append(c)

    def do_compute(self):
        self.load()

    def do_compute_ui(self, displayer, ask_refresh):
        if ask_refresh:
            self.c = widget.AdaptativeText(
                'Cloud connection is OK', 0, 0, 32, 8)
        displayer.display(self.c)

    def is_enough_displayed(self):
        return self.display_duration.is_triggered() and self.c.is_animation_end()


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
