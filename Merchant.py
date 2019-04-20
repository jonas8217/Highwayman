from Vector import Normalize, Vector as vect


class Merchant:
    def __init__(self, start_city, end_city, cargo):
        s_pos = vect(start_city.pos[0], start_city.pos[1])
        e_pos = vect(end_city.pos[0], end_city.pos[1])
        self.pos = vect(s_pos.x, s_pos.y)
        self.cargo = cargo
        self.speed = 0.1
        
        self.vel = Normalize(e_pos - s_pos)

    def move(self, p_pos = None):
        if p_pos == None:
            self.pos += self.vel

