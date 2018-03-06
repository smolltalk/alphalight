
class Window(object):

    def __init__(self, manager, x, y, w, h):
        self.__manager = manager
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.__transparent = False
        self.__visible = True
        self.__widgets = []

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        if visible != self.__visible:
            self.__visible = visible
            self.__fire_changed()

    @property
    def transparent(self):
        return self.__transparent

    @transparent.setter
    def transparent(self, transparent):
        if transparent != self.__transparent:
            self.__transparent = transparent
            self.__fire_changed()

    def add_widget(self, widget):
        self.__widgets.append(widget)
        if widget.visible:
            self.__fire_changed()

    def remove_widget(self, widget):
        self.__widgets.remove(widget)
        if widget.visible:
            self.__fire_changed()

    def clear_widgets(self):
        if len(self.__wigets) > 0:
            self.__widgets = []
            self.__fire_changed()

    def input_received(self, e):
        pass

    def clock_received(self, count):
        pass

    def __fire_changed(self):
        self.__manager.window_changed(self)


class WindowManager(object):

    def __init__(self):
        self.windows = []

    def new_window(self, x, y, w, h):
        window = Window(self, x, y, w, h)
        self.windows = self.windows.append(window)
        return window

    def move_to_window(self, forward=True):
        found = False
        for idx, w in enumerate(reversed(self.windows[:-1])):
            if w.visible:
                found = True
                break
        if found:
            i = len(self.windows) - idx - 2
            self.windows = self.windows[:i] + self.windows[(i + 1):] + [w]

    def is_displayable(self, window):
        if not window.visible:
            return False

        for w in self.windows:
            if w == window:
                continue
            if not w.visible or w.transparent:
                continue
            return window.x < w.x or window.y < w.y or (window.x + window.w) > (w.x + w.w) or (window.y + window.h) > (w.y + w.h)

    def window_changed(self, window):
        if self.need_refresh:
            return
        self.need_refresh = is_displayable(window)

    def display(self):
        for w in self.windows:
            if self.is_displayable(w):
                w.display()
            displayer.paste(x, y)

    def process(self):
        # Send clock event
        # Send input event
        # Display
