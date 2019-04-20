from random import randint
from math import ceil

class City:
    def __init__(self, pos):
        self.pos = pos
        self.size = randint(9,17)
        start_col = randint(100,215)
        self.col = (start_col + randint(0,80) - 40, start_col + randint(0,80) - 40, start_col + randint(0,80) - 40)
        r = []
        for i in range(ceil((self.size-9)/2)):
            r.append(randint(0,2))
        self.resources = [r.count(0),r.count(1),r.count(2)]


    def __repr__(self): #For debugging purposes
        return 'City: pos(' + str(self.pos[0]) + ',' + str(self.pos[1]) + ')'