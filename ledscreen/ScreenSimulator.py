import sys


class SimulatedBufferedScreen:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.buffer = [0] * w * h

    def size(self):
        return (self.w, self.h)

    def push(self, v):
        self.buffer = [v] + self.buffer[:-1]

    def push_image(self, image):
        arr = np.asarray(image)
        arr = np.where(arr, 0, 1)

        for a in arr:
            for b in a:
                self.screen.push(b)

    def flush(self):
        sys.stdout.write("\033[1;31m")
        i = self.w * self.h - 1
        for y in range(self.h):
            for x in range(self.w):
                if self.buffer[i] == 1:
                    sys.stdout.write(u'\u25cf ')
                else:
                    sys.stdout.write('  ')
                i = i - 1
            print("")
        sys.stdout.write("\033[8A")
        sys.stdout.write("\033[64D")
