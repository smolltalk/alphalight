# TODO
# Long OUT


class Widget(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.focusable = True
        self.selectable = True
        self.__transparent = False
        self.__visible = True

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

    @property
    def animation_ended(self):
        return self.is_animation_ended()

    def is_animation_ended(self):
        return True

    def __fire_changed(self):
        if self.parent:
            self.parent.on_widget_changed(self)

    def on_clock(self, count):
        pass

    def display(self, displayer):
        pass

    def on_focus(self):
        pass

    def on_unfocus(self):
        pass

    def on_select(self):
        pass

    def on_unselect(self):
        pass

    def on_input(self, e):
        pass


class Container(Widget):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.__widgets = []
        self.__focus_widget = None
        self.__selected_widget = None

    def add_widget(self, widget):
        widget.parent = self
        self.__widgets.append(widget)
        if widget.visible:
            self.__fire_changed()

    def remove_widget(self, widget):
        self.__widgets.remove(widget)
        widget.parent = None
        fire_change = False
        if widget is self.__selected_widget:
            fire_change = True
            self.unselect()

        if widget is self.__focus_widget:
            fire_change = True
            self.unfocus_widget()

        fire_change |= widget.visible

        if fire_change:
            self.__fire_changed()

    def clear_widgets(self):
        if len(self.__wigets) > 0:
            self.unselect()
            self.unfocus()
            self.__widgets = []
            self.__fire_changed()

    def focus(self, forward=True):
        found = False
        for idx, w in enumerate(reversed(self.__widgets[:-1])):
            if w.visible and w.focusable and w is not self.__focus_widget:
                found = True
                break

        if found:
            i = len(self.__widgets) - idx - 2
            self.__widgets = self.__widgets[:i] + \
                self.__widgets[(i + 1):] + [w]

            if self.__focus_widget:
                self.__focus_widget.on_unfocus()

            self.__focus_widget = w
            self.__focus_widget.on_focus()

    def unfocus(self):
        if self.__focus_widget:
            self.__focus_widget.on_unfocus()
            self.__focus_widget = None

    def select(self):
        if self.__selected_widget:
            return
        # Else
        w = self.__widgets[-1]
        if w.selectable:
            self.__selected_widget = w
            self.select.on_select()

    def unselect(self):
        if not self.__selected_widget:
            return
        # Else
        self.__selected_widget.on_unselect()
        self.__selected_widget = None

    def is_widget_displayable(self, widget):
        if not widget.visible:
            return False

        for w in self.__widgets:
            if w == widget:
                continue
            if not w.visible or w.transparent:
                continue
            return widget.x < w.x or widget.y < w.y or (widget.x + widget.w) > (w.x + w.w) or (widget.y + widget.h) > (w.y + w.h)

    def on_clock(self, count):
        for w in self.__widgets:
            w.on_clock(count)

    def display(self, displayer):
        for w in self.__widgets:
            if self.is_widget_displayable(w):
                wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
                w.display(wd)

    def on_widget_changed(self, widget):
        if self.__need_refresh:
            return
        self.__need_refresh = is_displayable(widget)

    def on_input(self, e):
        if self.__selected_widget:
            if e == Key.OUT and self.__selected_widget.input(e):
                self.unselect()
        else:
            if e == Key.PLUS or e == Key.MINUS:
                self.focus(e == Key.PLUS)
            elif e == Key.IN:
                self.select()
            elif e == Key.OUT
                return True
        return None


class WidgetManager(ContainerWidget):

    def __init__(self, screen):
        self.__screen = screen

    def display(self):
        # Prepare image
        w, h = self.__screen.size()
        image = PIL.Image.new('L', (w, h), 1)

        # Prepare displayer
        displayer = ImageDisplayer(image)

        for w in self.__widgets:
            if self.is_displayable(w):
                wd = ChildDisplayer(displayer, w.x, w.y, w.w, w.h)
                w.display(wd)

        # Push image to screen
        self.__screen.push_image(image)
        self.__screen.flush()

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
        self.parent_displayer = parent_displayer
        self.__rel_x = rel_x
        self.__rel_y = rel_y
        self.__w = w
        self.__h = h

    def paste(self, x, y, image)
    # TODO crop when needed
        self.parent_displayer.paste(
            self.__rel_x + x, self.__rel_y + y, image)


class StaticImage(Widget):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h)
        self.__set_image(image)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__set_image(image)
        self.__fire_changed()

    def __set_image(self, image)
        self.__image = image
        tw, th = image.size
        cropx = 0
        cropy = 0
        cropx2 = min(cropx + self.w, tw)
        cropy2 = min(cropy + self.h, th)
        self.crop__text_image = self.__image.crop(
            (cropx, cropy, cropx2, cropy2))

    def display(self, displayer):
        displayer.paste(0, 0, self.crop__text_image)


class ScrollingImage(Widget):

    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h)
        self.__set_image(image)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__set_image(image)
        self.__fire_changed()

    def __set_image(self, image)
        self.scroll_offset = 0
        tw, th = image.size
        self.scrolling_image = Image.new('L', (tw + w, th), 1)
        self.scrolling_image.paste(image, (0, 0))
        self.scrolling_image.paste(image, (tw, 0))
        self.tw, self.th = self.scrolling_image.size
        self.scrolling_size = self.tw - self.w

    def on_clock(self, count):
        cropx = self.scroll_offset
        cropy = 0
        cropx2 = min(cropx + self.w, self.tw)
        cropy2 = min(cropy + self.h, self.th)
        self.crop__text_image = self.scrolling_image.crop(
            (cropx, cropy, cropx2, cropy2))
        self.scroll_offset += 1
        self.scroll_offset %= self.scrolling_size
        self.__fire_changed()

    def display(self, displayer):
        displayer.paste(0, 0, self.crop__text_image)

    def is_animation_end(self):
        return self.scroll_offset == self.scrolling_size - self.w


class AdaptativeImage(Widget):
    def __init__(self, x, y, w, h, image):
        super().__init__(x, y, w, h)
        self.__set_image(image)

    @property
    def image(self):
        return self.sub_widget.image

    @image.setter
    def image(self, image):
        self.__set_image(image)
        self.__fire_changed()

    def __set_image(self, image)
        tw, th = image.size
        if tw < w:
            self.sub = StaticImage(x, y, w, h, image)
        else:
            self.sub = ScrollingImage(x, y, w, h, image)
        self.sub.parent = self

    def display(self, displayer):
        self.sub.display(displayer)


PLATFORM_FONT_DIR = {'win32': 'c:\\windows\\fonts\\',
                     'darwin': '/Library/Fonts/', 'linux': '', 'linux2': ''}


class AdaptativeText(Widget):
    # TODO text format
    # TODO disable auto scrolling

    def __init__(self, x, y, w, h, text, font_name='PressStart2P-Regular', font_size=8, font_dir=None):
        super().__init__(x, y, w, h)
        # http://www.fontsc.com/font/category/pixel-bitmap/8px?page=2
        # text_image = utils.text_to_image(text, '/Library/Fonts/Arial Bold.ttf', 10)
        # arialbd.ttf', 10)
        # Good for text shift: PressStart2P-Regular.ttf', 8)
        # Memoria.ttf', 7)
        # MiniTot.ttf', 8)
        # type_writer.ttf', 8)
        # teacp__.ttf', 7)
        # Good for number : Fleftex_M.ttf', 8) Emulator.ttf', 8)
        # pixearg.ttf', 8) pixeab_.ttf', 8)
        # fixed_bo.ttf', 6)
        # fixed_v0.ttf', 4) 02
        # fixed_v0_0.ttf', 8) 01
        # serif_v0.ttf', 6)
        # swf!t__.ttf', 8)

        if not font_dir:
            self.font_dir = PLATFORM_FONT_DIR[platform]
        self.font_name = font_name
        self.font_size = font_size
        self.__set_text(text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__set_text(text)
        self.__fire_changed()

    def __set_text(self, text):
        self.__text = text
        text_image = utils.text_to_image(
            self.__text, self.font_dir + self.font_name + '.ttf', self.font_size)

        tw, th = text_image.size
        if tw < self.w:
            self.sub = StaticImage(
                text_image, self.x, self.y, self.w, self.h)
        else:
            scrolling_image = Image.new('L', (tw + self.w, th), 1)
            scrolling_image.paste(text_image, (0, 0))
            self.sub = ScrollingImage(
                scrolling_image, self.x, self.y, self.w, self.h)
        self.sub.parent = self

    def display(self, displayer):
        self.sub.display(displayer)

    def is_animation_end(self):
        return self.sub.is_animation_end()


class AdaptativeNumeric(Widget):
    # TODO value format
    # TODO disable auto scrolling

    def __init__(self, x, y, w, h, value, value_min, value_max, font_name='Fleftex_M', font_size=8, font_dir=None):
        super().__init__(x, y, w, h)
        self.value_min = value_min
        self.value_max = value_max
        self.sub = AdaptativeText(
            x, y, w, h, '', font_name, font_size, font_dir)
        self.__set_value(value)
        self.sub.parent = self

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):

    def __set_value(self, value)
        if self.value_max < self.value_min:
            raise Exception(
                'Value_max ({}) is less than value_min ({})'.format(self.value_max, self.value_min))
        if value < self.value_min:
            raise Exception(
                'Value ({}) is less than min ({})'.format(value, self.value_min))
        if value > self.value_max:
            raise Exception(
                'Value ({}) is greater than min ({})'.format(value, self.value_min))

        self.__value = value
        self.sub.text = str(self.__value)

    def display(self, displayer):
        self.sub.display(displayer)

    def is_animation_end(self):
        return self.sub.is_animation_end()


# class NumericInput(AdaptativeNumeric):

#     def input_in(self):
#         self.is_blinking = True

#     def input_out(self):
#         self.is_blinking = False

#     def input(self, key):
#         if key == g.Key.PLUS:
#             if self.value < self.value_max:
#                 self.value += 1
#             else:
#                 self.value = self.value_min

#         elif key == g.Key.MINUS:
#             if self.value > self.value_min:
#                 self.value -= 1
#             else:
#                 self.value = self.value_max


# CHAR_LIST = list(re.sub('\t\s*', '', string.printable))
# CMD_INSERT = '[+]'
# CMD_DELETE = '[>]'
# CMD_LIST = [CMD_INSERT, CMD_DELETE]


# class TextInput(Widget):

#     def __init__(self, parent, x, y, w, h, text, font_name='PressStart2P-Regular', font_size=8, font_dir=None):
#         self.cursor_pos = 0
#         self.char_orig = 0
#         self.char_idx = 0
#         self.command_idx = 0
#         self.command_mode = False
#         self.text_component = AdaptativeText(
#             '', x, y, w, h, font_name, font_size, font_dir)
#         self.text = text

#     @property
#     def text(self):
#         return self.__text

#     @text.setter
#     def text(self, val):
#         self.__text = val
#         val_len = len(val)
#         if val_len == 0:
#             self.enter_command_mode()
#         else:
#             if self.cursor_pos > val_len:
#                 self.cursor_pos = val_len
#                 self.enter_command_mode()
#             else:
#                 self.enter_command_mode()
#         self.compute_display__text()

#     def enter_command_mode(self, start_end=False):
#         if start_end:
#             self.command_idx = len(CMD_LIST) - 1
#         else:
#             self.command_idx = 0
#         self.command_mode = True

#     def enter_char_mode(self):
#         self.char_orig = __text[self.cursor_pos]
#         self.char_idx = CHAR_LIST.index(self.char_orig)
#         self.command_mode = False

#     def is_over__text(self):
#         text_len = len(self.text)
#         if text_len == 0:
#             return True
#         if self.cursor_pos == text_len:
#             return True

#         return False

#     def move_cursor(self, delta):
#         self.cursor_pos = (self.cursor_pos + delta) % (len(self.text) + 1)
#         if self.cursor_pos == len(self.text):
#             self.enter_command_mode()
#         self.compute_display__text()

#     def shift_char(self, delta):
#         if self.command_mode:
#             self.command_idx += delta
#             if self.command_idx == -1 or self.command_idx == len(CMD_LIST):
#                 if self.is_over__text():
#                     self.enter_command_mode(start_end=(self.command_idx == -1))
#                 else:
#                     self.enter_char_mode()
#         else:
#             self.char_idx += delta
#             if self.char_idx >= 0 and self.char_idx < len(CHAR_LIST):
#                 # Modify text
#                 self.__text[self.cursor_pos] = CHAR_LIST[self.char_idx]
#             else:
#                 # Restore orig char
#                 self.__text[self.cursor_pos] = self.char_orig
#                 # Enter in command mode
#                 self.enter_cmd_mode(start_end=(self.char_idx == -1))

#         self.compute_display__text()

#     def interpret_command(self):
#         if CMD_LIST[self.command_idx] == CMD_INSERT:
#             self.insert_char()
#         elif CMD_LIST[self.command_idx] == CMD_DELETE:
#             self.delete_char()

#     def insert_char(self):
#         text = self.text
#         text = text[:self.cursor_pos] + \
#             'a' + text[self.cursor_pos:]
#         self.cursor_pos += 1
#         self.text = text

#     def delete_char(self):
#         if not self.is_over__text():
#             text = self.text
#             self.text = text[:self.cursor_pos] + \
#                 text[(self.cursor_pos + 1):]
#         self.compute_display__text()

#     def input_in(self):
#         pass

#     def input_out(self):
#         pass

#     def input(self, key):
#         if key == g.Key.PLUS:
#             self.shift_char(1)

#         elif key == g.Key.MINUS:
#             self.shift_char(-1)

#         elif key == g.Key.IN:
#             if self.command_mode:
#                 self.interpret_command()
#             else:
#                 self.move_cursor(1)

#         return None

#     def compute_display__text(self):
#         if self.command_mode:
#             display__text = self.__text[:self.cursor_pos] + \
#                 CMD_LIST[self.char_idx] + self.__text[self.cursor_pos:]
#         else:
#             dispay__text = self.__text
#         self.text_component.text = display__text

#     def display(self, displayer):
#         return self.text_component.display(displayer)

#     def is_animation_end(self):
#         return self.text_component.is_animation_end()
