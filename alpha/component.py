from ledscreen import *
from ledscreen import getch as g
from enum import Enum, auto
from datetime import datetime
from copy import copy
import threading as th
import json
import time

# TODO consolidate compute_ui and draw?


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


class Blinker(object):
    def __init__(self):
        self.counter = 0
        self.blink = False
        self.has_changed = False

    def tick(self):
        prev_blink = self.blink
        self.blink = self.counter % 10 < 5
        blink_changed = prev_blink != self.blink


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


class PropertyNode(object):
    def __init__(self, name, obj, parent=None):
        self.name = name
        self.parent = parent
        self.properties = {}
        self.value = 'value'
        if isinstance(obj, str):
            self.type = 'string'
        elif isinstance(obj, dict):
            if '__type' in obj.keys():
                self.type = obj['__type']
            else:
                self.type = 'object'
            if self.type == 'object':
                for property_name in obj.keys():
                    if not property_name.startswith('__'):
                        self.properties[property_name] = PropertyNode(
                            property_name, obj[property_name], self)
            else:
                if '__value' in obj.keys():
                    self.value = obj['__value']

    def is_root(self):
        return self.parent == None

    def has_properties(self):
        return len(self.properties) > 0

    def property(self, property_name):
        return self.properties[property_name]

    def property_first(self):
        if len(self.properties) == 0:
            return None
        return self.properties[list(self.properties.keys())[0]]

    def property_after(self, property_name, delta):
        if len(self.properties) == 0:
            return None
        key_list = list(self.properties.keys())
        i = key_list.index(property_name)
        i = (i + delta) % len(key_list)
        return self.properties[key_list[i]]


class PropertyNodeBrowser(object):

    def __init__(self, node):
        self.node = node

    def compute_ui(self, displayer):
        displayer.display(self.component)

    def move_to(self, node):
        if node is self.node:
            return
        self.node = node
        self.component = widget.AdaptativeText(
            node.name + ': ' + node.value, 0, 0, 32, 8)

    def input(self, event):
        type = event['type']
        if type == 'key':
            key = event['key']
            if key == g.Key.PLUS or key == g.Key.MINUS:
                if not self.node.is_root():
                    self.move_to(self.node.parent.property_after(
                        self.node.name, 1 if key == g.Key.PLUS else -1))
            elif key == g.Key.IN:
                if self.node.has_properties():
                    self.move_to(node.property_first)
                    return self
                else:
                    pass
                    # switch in edit mode
            elif key == g.Key.OUT:
                if not self.node.is_root():
                    self.move_to(self.node.parent)
        elif type == 'focus_in':
            self.move_to(self.node.property_first())


class AlphaComponent(object):

    def __init__(self, interactive=False, config=None, configurable=False, compute_period=600, compute_ui_period=1, display_duration_sec=5):
        self.interactive = interactive
        self.config = config
        self.configurable = configurable
        self.compute_trigger = PeriodicTrigger(compute_period)
        self.compute_ui_trigger = PeriodicTrigger(compute_ui_period)
        self.display_duration = DurationTrigger(display_duration_sec)
        self._data = None
        self._data_changed = False
        self.configuring = False

    def compute_data(self):
        if self.compute_trigger.tick():
            prev_data = self._data
            self._data = self.do_compute_data(copy(self._data))
            self._data_changed = prev_data != self._data

    def compute_ui(self, displayer, ask_refresh):
        if ask_refresh:
            self.compute_ui_trigger.reset()
            self.display_duration.reset()

        if self.configuring:
            self.configurer.compute_ui(displayer)
        else:
            if self.compute_ui_trigger.tick():
                self.do_compute_ui(displayer, ask_refresh, self._data,
                                   self._data_changed, self.compute_ui_trigger.counter)
                self._data_changed = False

    def is_enough_displayed(self):
        return self.display_duration.is_triggered()

    def is_interactive(self):
        return self.interactive

    def is_configurable(self):
        return self.configurable and self.config

    def enter_configuring(self):
        if not self.config:
            return
        config_node = PropertyNode('conf', self.config)
        self.configurer = PropertyNodeBrowser(config_node)
        self.configuring = True
        return self.configurer

    def do_compute_data(self, data):
        pass

    def do_compute_ui(self, displayer, ask_refresh, data, data_changed):
        pass

    def input(self, event):
        type = event['type']
        if type == 'key':
            key = event['key']
            if key == g.Key.IN:
                return self.enter_configuring()


class SliderComponent(AlphaComponent):
    def __init__(self, component_manager):
        super().__init__(interactive=True)
        self.component_manager = component_manager
        self.component_list = []
        self.component = None
        self.component_selected = False
        self.index = -1
        self.size = 1

    def get_list(self):
        self.component_list = self.component_manager.get_list()
        self.size = len(self.component_list)

    def move_to(self, delta=1):
        self.index = (self.index + delta) % self.size
        if self.index == 0:
            self.get_list()

        return self.component_list[self.index]

    def input(self, event):
        type = event['type']
        if type == 'key':
            key = event['key']
            if key in [g.Key.PLUS, g.Key.MINUS]:
                previous_component = self.component
                self.component = self.move_to(1 if key == g.Key.PLUS else -1)
                self.component_changed |= self.component != previous_component
            elif key == g.Key.IN:
                if self.component.is_interactive():
                    return self.component
                else:
                    return None
        elif type == 'focus_lost':
            self.component_selected = True
        elif type == 'focus_back':
            self.component_selected = False

    def compute_state(self):
        if self.component is None:
            self.component = self.move_to()
            self.component_changed = True
        elif self.component_selected:
            return
        elif self.component.is_enough_displayed():
            previous_component = self.component
            self.component = self.move_to()
            self.component_changed |= self.component != previous_component

    def do_compute_ui(self, displayer, ask_refresh, data, data_changed, counter):
        self.compute_state()
        self.component.compute_ui(displayer, self.component_changed)
        self.component_changed = False


class TimeComponent(AlphaComponent):

    def __init__(self):
        super().__init__(interactive=True, config={'Toto': 'toto',
                                                   'Titi': 'titi'}, configurable=True)
        self.hour = None

    def do_compute_ui(self, displayer, ask_refresh, data, data_changed, counter):
        hour = datetime.now().strftime('%H:%M')
        if self.hour != hour or ask_refresh:
            self.hour = hour
            c = widget.AdaptativeText(
                hour, 0, 0, 32, 8, font_name='Fleftex_M')
            displayer.display(c)


class AlarmComponent(AlphaComponent):
    # TODO blink management in component?
    # TODO manage data based on this component behavior
    # TODO data store

    def __init__(self):
        super().__init__()

    def do_compute_ui(self, displayer, ask_refresh, data, data_changed, counter):
        pass


class ComponentManager(AlphaComponent):

    # TODO Load file data in str and use it to detect change

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

    def do_compute_data(self, data):
        self.load()

    def do_compute_ui(self, displayer, ask_refresh, data, data_changed, counter):
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
            c.compute_data()

    def run(self):
        while not self.stopper.wait(.01):
            self.compute()
