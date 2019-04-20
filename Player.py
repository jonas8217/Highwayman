from Vector import Vector as vect

class Player:
    def __init__(self, x, y):
        self.pos = vect(x, y)
        self.speed = 2

    def move (self, vel, speed_modifier = 1):
        self.pos += vel * self.speed * speed_modifier

    