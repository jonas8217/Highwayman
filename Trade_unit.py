from Vector import Normalize, Vector as vect
from math import cos,sin,pi
from Dist import dist

class Trade_unit():
    def __init__(self, start_city, end_city, cargo, time, guards = 0):
        s_pos = vect(start_city.pos[0], start_city.pos[1])
        e_pos = vect(end_city.pos[0], end_city.pos[1])
        self.end_city = end_city
        self.pos = vect(s_pos.x, s_pos.y)
        self.cargo = cargo
        self.speed = 0.1
        self.max_hp = 10
        self.hit_points = self.max_hp
        self.detect_dist = 12
        
        self.vel = Normalize(e_pos - s_pos)
        self.guards = []
        if guards > 0:
            self.guards = assign_guards(guards, self.vel, time)


    def move(self, player):
        if player is not None:
            if len(self.guards) > 0:
                for guard in self.guards:
                    guard.move(self.pos, player)
            else:
                self.pos += self.vel * self.speed * 1.2
        else:
            origin = True
            for guard in self.guards:
                if dist(guard.original_rel_pos, guard.rel_pos) > 0.15:
                    origin = False
            if origin == True:
                self.pos += self.vel * self.speed
            else:
                for guard in self.guards:
                    guard.move(self.pos)

    def check_if_guard_dead(self, guard):
        if guard.hit_points <= 0:
            self.guards.remove(guard)
            


def assign_guards(num, direc, time):
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
        guards.append(Guard(g_pos, time))
    return guards

class Guard:
    def __init__(self, rel_pos, time):
        x, y = rel_pos.x, rel_pos.y
        self.rel_pos = vect(x,y)
        self.original_rel_pos = vect(x,y)
        self.pos = None
        self.end_city = None
        self.speed = 0.1
        self.max_hp = 15
        self.hit_points = self.max_hp
        self.detect_dist = 6
        self.damage = 3
        self.attack_range = 1.5
        self.attack_rate = 2.5
        self.attack_duration = 0.15
        self.last_attacked = time

    def move(self, guarding_pos, player = None):
        if self.pos is None:
            if player is not None:
                pos = self.rel_pos + guarding_pos
                p_pos = player.pos
                if dist(pos, p_pos) > self.attack_range:
                    vel = Normalize(p_pos - pos)
                    self.rel_pos += vel * self.speed
            else:
                vel = Normalize(self.original_rel_pos - self.rel_pos)
                self.rel_pos += vel * self.speed
        else:
            if player is not None:
                p_pos = player.pos
                if dist(self.pos, p_pos) > self.attack_range:
                    vel = Normalize(p_pos - self.pos)
                    self.pos += vel * self.speed
            else:
                vel = Normalize(vect(self.end_city.pos[0], self.end_city.pos[1]) - self.pos)
                self.pos += vel * self.speed

    def attack(self, target):
        target.hit_points -= self.damage
