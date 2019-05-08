

class Trap:
    def __init__(self,pos):
        self.pos = pos
        self.damage = 12

    def attack(self, target):
        target.hit_points -= self.damage
