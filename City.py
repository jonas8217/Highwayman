from random import randint

class City:
    def __init__ (self, pos):
        self.pos = pos
        self.size = randint(11,15)
        start_col = randint(100,215)
        self.col = (start_col + randint(0,80) - 40, start_col + randint(0,80) - 40, start_col + randint(0,80) - 40)