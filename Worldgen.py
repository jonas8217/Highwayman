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

        #Confine variabels
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
                #tile = p[x][y]
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
            if self.tiles[pos[0]][pos[1]][0] == 2: # Checks if city bouandaries are okay
                if self.tiles[pos[0]][pos[1]-4][0] == self.tiles[pos[0]-4][pos[1]][0] == self.tiles[pos[0]+4][pos[1]][0] == self.tiles[pos[0]][pos[1]+4][0] == 2:
                    good_pos = True
                    for city in self.cities:
                        if dist(pos, city.pos) < 25:
                            good_pos = False
                    if good_pos:
                        self.cities.append(City(pos))
        
        # Road generation
        dists = []
        for c1 in self.cities:                                      # Generating list of all possible city connections and the length thereof
            for c2 in self.cities:                                  #
                if c1 is not c2:                                    #
                    dists.append((c1, c2, dist(c1.pos, c2.pos)))    # Create touple of 2 cities and distance: (c1, c2, float: 'distance') and adds them to 'dists' list
        
        connections = [] # Connected cites
        unfound = self.cities.copy() # Unconnected cities
        
        s_dist = shortets_dist(dists)

        connections.append(s_dist)            # Append to new connection to connections
        unfound.pop(unfound.index(s_dist[0])) # and
        unfound.pop(unfound.index(s_dist[1])) # Remove now found city
        
        while len(unfound) != 0: #Keeps going until there are no more unfound citites (all cities are found)
            cons = []
            
            # Finds the shortest connection which has both a connection to 'connected' and to 'unfound' insuring a correct connection
            for con in connections: 
                for dis in dists:
                    if (con[0] in dis or con[1] in dis) and (dis[0] in unfound or dis[1] in unfound): 
                        cons.append(dis)

            s_dist = shortets_dist(cons)
            
            connections.append(s_dist)              # Add new connection

            i = 0                                   # Delete city from unfound 
            if s_dist[1] in unfound:                #
                i = 1                               #
            unfound.pop(unfound.index(s_dist[i]))   #

        for c in connections:                       # Create road objects and add to self.roads
            self.roads.append(Road(c[0], c[1]))     #
        

def dist(P1, P2):
    # Returns distance between 2 points
    return sqrt(((P1[0] - P2[0])**2) + ((P1[1] - P2[1])**2))

def uniq(lst):
    # Returns a duplicateless list
    seen = set()
    uniq = []
    for i in lst:
        if i not in seen:
            uniq.append(i)
            seen.add(i)
    return uniq

def shortets_dist(dists):
    # Finds the 'dist' touple with the smallest distance value
    shortest = None
    for d in dists:
        if shortest == None:
            shortest = d
        elif d[2] < shortest[2]:
            shortest = d
    return shortest

