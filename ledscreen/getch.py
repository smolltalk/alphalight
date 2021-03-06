from enum import Enum
import threading as th


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        return sys.stdin.read(1)


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class Key(Enum):
    IN = 0
    OUT = 1
    PLUS = 2
    MINUS = 3
    LONG_IN = 4
    LONG_OUT = 5
    LONG_PLUS = 6
    LONG_MINUS = 7
    QUIT = 8


class KeyReader(th.Thread):
    def __init__(self, stopper=th.Event()):
        super().__init__()
        self.daemon = True
        self.stopper = stopper
        self.key = None

    def stop(self):
        self.stopper.set()

    def read_key(self):
        # TODO Need some sync
        ret = self.key
        self.key = None
        return ret

    def run(self):
        inkey = _Getch()
        while not self.stopper.isSet():
            k = inkey()
            if k == b'-' or k == '-':
                self.key = Key.MINUS
            elif k == b'+' or k == '+':
                self.key = Key.PLUS
            elif k == b'i' or k == 'i':
                self.key = Key.IN
            elif k == b'o' or k == 'o':
                self.key = Key.OUT
            elif k == b'q' or k == 'q':
                self.key = Key.QUIT
