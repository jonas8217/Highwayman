from Perlin import perlingrid as pGrid
from City import City
from Road import Road
from math import ceil,tanh,sqrt
from random import randint
import numpy as np



class World_map:
    def __init__(self, w, h, tile_size, seed, size):
        self.tiles = []
        self.width = w
        self.height = h
        self.tile_size = tile_size
        self.seed = seed
        self.size = size

        self.cities = []
        self.roads = []

        #confine variabels
        if size < 1:
            size = 1
        elif size > 10:
            size = 10

        self.dimensions = w
        if w < h:
            self.dimensions = h
        
        #Generate map
        
        p = pGrid(size, self.dimensions, self.seed)

        #Find extremedies
        i,j = np.unravel_index(p.argmin(), p.shape)
        min_val = p[i,j]
        i,j = np.unravel_index(p.argmax(), p.shape)
        max_val = p[i,j]

        size_val = max_val
        if size_val < abs(min_val):
            size_val = abs(min_val)

        for x in range(w):
            self.tiles.append([])
            for y in range(h):
                tile = tanh(p[x][y]/(0.45*(size_val/0.5)))*0.5+0.5
                """
                if (x, y) == max_pos:
                    b_type = (-1, (255,0,0))
                elif (x, y) == min_pos:
                    b_type = (-1, (255,255,0))
                """
                if tile < 0.2:
                    b_type = (0, (13 - tile * 54, 61 - tile * 57, 120 - tile * 61), 0.2) #Water
                elif tile < 0.22:
                    b_type = (1, (246, 220, 55), 0.75) #Beach
                elif tile < 0.65:
                    b_type = (2, (146, 203, 54), 1.25) #Grassland
                elif tile < 0.7:
                    b_type = (3, (107, 164, 15), 1) #Highlands
                elif tile < 0.8:
                    b_type = (4, (-45 * (tile-0.7)*10 + 140, -45 * (tile-0.7)*10 + 140, -45 * (tile-0.7)*10 + 140), 0.6) #Mountain
                else:
                    b_type = (5, (55 * (tile-0.8)*5 + 200, 55 * (tile-0.8)*5 + 200, 55 * (tile-0.8)*5 + 200), 0.45) #Mountain_top_snow
                self.tiles[x].append(b_type)

        # City generation
        for i in range(100):
            pos = (randint(8,w-8), randint(8,h-8))
            if self.tiles[pos[0]][pos[1]][0] == 2: # checks if city bouandaries are okay
                if self.tiles[pos[0]][pos[1]-4][0] == self.tiles[pos[0]-4][pos[1]][0] == self.tiles[pos[0]+4][pos[1]][0] == self.tiles[pos[0]][pos[1]+4][0] == 2:
                    good_pos = True
                    for city in self.cities:
                        if dist(pos, city.pos) < 25:
                            good_pos = False
                    if good_pos:
                        self.cities.append(City(pos))
        
        # Road generation
        road_map = []
        for c1 in self.cities:
            closest = None
            for c2 in self.cities:
                if c1 is not c2:
                    if closest is None:
                        closest = c2
                    elif dist(c1.pos, c2.pos) < dist(c1.pos, closest.pos):
                        closest = c2
            road_map.append([[c1.pos, closest.pos]])

        for bunch in road_map:
            for road in bunch:
                for other_bunch in road_map:    
                    if bunch is not other_bunch:
                        for other_road in other_bunch:
                            if road[0] in other_road or road[1] in other_road:
                                bunch.append(other_road)
                                other_bunch.pop(other_bunch.index(other_road))
        j = 0
        for i in range(len(road_map)):
            if len(road_map[i - j]) == 0:
                road_map.pop(i - j)
                j += 1
        print(road_map)
        
        for i in range(len(road_map)):
            road_map[i] 
            
        print(road_map)
    

        
        

        """
        while len(connections) > 1:
            for c in connections:
                closest_pair = None
                for otherc in connections:
                    
                    if c is not otherc:
                        for p1 in c:
                            for p2 in otherc:
                                
                                if closest_pair is None:
                                    closest_pair = (p1, p2)
                                elif dist(p1, p2) < dist(p1, closest):
                                    closest_pair = (p1, p2)
                
                connections.append(closest_pair[0].pos, closest_pair[1].pos)
        """
        
        


def dist(P1,P2):
    return sqrt(((P1[0] - P2[0])**2) + ((P1[1] - P2[1])**2))

def unique(lst):
    seen = set()
    unique = []
    for i in lst:
        if i not in seen:
            unique.append(i)
            seen.add(i)
    return unique