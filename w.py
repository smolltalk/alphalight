# TODO
# - Widget
# - ContainerWidget
#   - with option on sub widget component order
#   - dispatch display, clock, input_received
#   - fire change to parent


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
        if widget == self.selected_widget:
            self.unselect_widget()
        if widget.visible:
            self.__fire_changed()

    def clear_widgets(self):
        if len(self.__wigets) > 0:
            self.unselect_widget()
            self.__widgets = []
            self.__fire_changed()

    def move_to_widget(self, forward=True):
        pass

    def select_widget(self):
        if self.widget_selected:
            return
        # Else
        self.selected_widget = self.active_widget
        self.widget_selected = True

    def unselect_widget(self):
        if not self.widget_selected:
            return
        # Else
        self.selected_widget = None
        self.widget_selected = False

    def display(self, displayer):
        for w in self.__widgets:
            wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
            w.display(wd)

    def input_received(self, e):
        if self.widget_selected:
            if not self.selected_widget.input(e):
                self.unselect_widget()
        else:
            if e == Key.PLUS or e == Key.MINUS:
                self.move_to_widget(e == Key.PLUS)
            elif e == Key.IN:
                self.select_widget()
            elif e == Key.OUT
                return False
        return None

    def clock_received(self, count):
        pass

    def __fire_changed(self):
        self.__manager.window_changed(self)


class WindowManager(object):

    def __init__(self, screen):
        self.__screen = screen
        self.__windows = []

    def new_window(self, x, y, w, h):
        window = Window(self, x, y, w, h)
        self.__windows = self.windows.append(window)
        return window

    def move_to_window(self, forward=True):
        found = False
        for idx, w in enumerate(reversed(self.__windows[:-1])):
            if w.visible:
                found = True
                break
        if found:
            i = len(self.__windows) - idx - 2
            self.__windows = self.__windows[:i] + \
                self.__windows[(i + 1):] + [w]

    def is_displayable(self, window):
        if not window.visible:
            return False

        for w in self.__windows:
            if w == window:
                continue
            if not w.visible or w.transparent:
                continue
            return window.x < w.x or window.y < w.y or (window.x + window.w) > (w.x + w.w) or (window.y + window.h) > (w.y + w.h)

    def window_changed(self, window):
        if self.__need_refresh:
            return
        self.__need_refresh = is_displayable(window)

    def select_window(self):
        if self.window_selected:
            return
        # Else
        self.selected_window = self.__windows[-1]
        self.window_selected = True

    def unselect_window(self):
        if not self.window_selected:
            return
        # Else
        self.selected_window = None
        self.window_selected = False

    def display(self):
        # Prepare image
        w, h = self.__screen.size()
        image = PIL.Image.new('L', (w, h), 1)

        # Prepare displayer
        displayer = ImageDisplayer(image)

        for w in self.__windows:
            if self.is_displayable(w):
                wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
                w.display(wd)

        # Push image to screen
        self.__screen.push_image(image)
        self.__screen.flush()

    def dispatch_clock(self):
        for w in self.__windows:
            w.clock_received()

    def input_received(self, e):
        if self.window_selected:
            if self.selected_window.input(e) == False:
                self.unselect_window()
        else:
            if e == Key.PLUS or e == Key.MINUS:
                self.move_to_window(e == Key.PLUS)
            elif e == Key.IN:
                self.select_window()

    def process(self):
        self.dispatch_clock()
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
