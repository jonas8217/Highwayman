from Vector import Normalize, Vector as vect
from math import cos,sin,pi

class Trade_unit():
    def __init__(self, start_city, end_city, cargo, guards = 0):
        s_pos = vect(start_city.pos[0], start_city.pos[1])
        e_pos = vect(end_city.pos[0], end_city.pos[1])
        self.pos = vect(s_pos.x, s_pos.y)
        self.cargo = cargo
        self.speed = 0.1
        self.hit_points = 10
        self.detect_dist = 7
        
        self.vel = Normalize(e_pos - s_pos)
        self.guards = []
        if guards > 0:
            self.guards = assign_guards(guards, self.vel)


    def move(self, p_pos):
        if p_pos is not None:
            if len(self.guards) > 0:
                for guard in self.guards:
                    guard.move(p_pos, self.pos)
            else:
                self.pos += self.vel * self.speed * 1.2
        else:
            self.pos += self.vel * self.speed
            


def assign_guards(num, direc):
    guards = []
    rotation = (2*pi)/num
    offset = 0
    if num % 2 == 0:
        offset = rotation/2
    x,y = direc.x, direc.y
    for i in range(num):
        phi = offset + rotation * i
        x_pos, y_pos= x * cos(phi) - y * sin(phi), x * sin(phi) + y * cos(phi)
        g_pos = vect(x_pos * 1.5, y_pos * 1.5)
        guards.append(Guard(g_pos))
    return guards

class Guard:
    def __init__(self,rel_pos):
        self.rel_pos = rel_pos
        self.speed = 0.1
        self.hit_points = 15
        self.damage = 3

    def move(self, p_pos, guarding_pos):
        pos = self.rel_pos + guarding_pos
        vel = Normalize(p_pos - pos)
        self.rel_pos += vel * self.speed
