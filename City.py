from random import randint
from math import ceil

class City:
    def __init__(self, pos):
        self.pos = pos
        self.roads = []
        self.weight = randint(0,9)
        self.size = self.weight + 8
        start_color = randint(100,215)
        self.color = (start_color + randint(0,80) - 40, start_color + randint(0,80) - 40, start_color + randint(0,80) - 40)
        self.sorted_resources = [0,0,0]
        for i in range(ceil(self.weight/2)):
            self.sorted_resources[randint(0,2)] += 1
        self.resources = []
        for i in range(3):
            for j in range(self.sorted_resources[i]):
                self.resources.append(i)
        


    def __repr__(self): #For debugging purposes
        return 'City: pos(' + str(self.pos[0]) + ',' + str(self.pos[1]) + ')'