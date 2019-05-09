from math import atan2, pi, acos, sqrt, cos, sin
from Vector import Vector, Dot, LengthSqrd

def vect_to_angle(v):
    x,y = v[0],v[1]

    if x == 0 and y == 0:
        return 0
    else:
        return atan2(y,x)

def vectors_to_angle(v1, v2):
    return acos(Dot(v1,v2)/(sqrt(LengthSqrd(v1)*LengthSqrd(v2))))

def angle_to_vector(a):
    return Vector(cos(a), sin(a))
