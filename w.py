
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

    def display(self, displayer):
        for w in self.__widgets:
            wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
            w.display(wd)

    def input_received(self, e):
        pass

    def clock_received(self, count):
        pass

    def __fire_changed(self):
        self.__manager.window_changed(self)


class WindowManager(object):

    def __init__(self, screen):
        self.screen = screen
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
        # Prepare image
        w, h = self.screen.size()
        image = PIL.Image.new('L', (w, h), 1)

        # Prepare displayer
        displayer = ImageDisplayer(image)

        for w in self.windows:
            if self.is_displayable(w):
                wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
                w.display(wd)

        # Push image to screen
        screen.push_image(image)
        screen.flush()

    def process(self):
        # Send clock event
        # Send input event
        self.display()


class ImageDisplayer(object):

    def __init__(self, image):
        self.__image = image

    def paste(self, x, y, image):
        self.__image.paste(image, (x, y))


class ChildDisplayer(object):

    def __init__(self, parent_displayer, rel_x, rel_y, w, h):
        self.__parent_displayer = parent_displayer
        self.__rel_x = rel_x
        self.__rel_y = rel_y
        self.__w = w
        self.__h = h

    def paste(self, x, y, image)
    # TODO crop when needed
        self.__parent_displayer.paste(
            self.__rel_x + x, self.__rel_y + y, image)
