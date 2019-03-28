from random import randint

class City:
    def __init__ (self, pos, size):
        self.pos = pos
        self.size = size
        start_col = randint(100,215)
        self.col = (start_col + randint(0,80) - 40, start_col + randint(0,80) - 40, start_col + randint(0,80) - 40)