from math import sqrt

def dist(P1, P2):
    # Returns distance between 2 points
    return sqrt(((P1[0] - P2[0])**2) + ((P1[1] - P2[1])**2))