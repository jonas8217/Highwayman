from math import atan2

def vect_to_rad(vector):
    x,y = vector[0],vector[1]

    if x == 0 and y == 0:
        return 0
    else:
        return atan2(y,x)