from Vector import Vector as vect
from Vector_to_radians import vect_to_rad

class Player:
    def __init__(self, x, y):
        self.pos = vect(x, y)
        self.speed = 2
        self.hit_points = 20
        self.damage = 4
        self.saturation = 10
        self.gold = 0
        self.provisions = 10
        self.materials = 0
        self.rotation = 90
        

    def move (self, vel, speed_modifier = 1):
        self.pos += vel * self.speed * speed_modifier
        self.rotation = vect_to_rad(vel)

    