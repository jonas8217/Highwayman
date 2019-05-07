from Vector import Vector as vect
from Vector_math import vect_to_angle

class Player:
    def __init__(self, x, y, time):
        self.pos = vect(x, y)
        self.speed = 0.15
        self.max_hp = 30
        self.hit_points = self.max_hp
        self.damage = 4
        self.attack_range = 2.5
        self.attack_rate = 0.5
        self.attack_duration = 0.15
        self.last_attacked = time
        self.gold = 0
        self.provisions = 10
        self.materials = 0
        self.rotation = 0
        

    def move(self, vel, speed_modifier = 1):
        self.pos += vel * self.speed * speed_modifier
        if not (vel[0] == 0 and vel[1] == 0):
            self.rotation = vect_to_angle(vel)

    def attack(self, target):
            target.hit_points -= self.damage


    