from Perlin import perlingrid as pGrid
from math import ceil,tanh
import numpy as np



class World_map:
    def __init__(self, w, h, tile_size, seed, size):
        self.tiles = []
        self.width = w
        self.height = h
        self.tile_size = tile_size
        self.seed = seed
        self.size = size

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