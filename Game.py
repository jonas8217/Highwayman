from math import pi, cos, sin, sqrt
from random import randint
from highscoreLogger import Logger
from Worldgen import World_map
from Player import Player
from Vector import Normalize,Vector as vect
import pickle




class Game:
    def __init__(self):
        self.state = 0

        self.world_map = None
        
        self.player = None

    def tick(self, pg, pressed):
        if self.state == 0.5:
            if pressed[pg.K_r]:
                self.generate_world(200,150,4,randint(1,500),3)
        
        if self.state == 1:

            #controls
            vel = vect(0, 0)
            if pressed[pg.K_UP]:
                vel += vect(0, -1)
            if pressed[pg.K_DOWN]:
                vel += vect(0, 1)
            if pressed[pg.K_LEFT]:
                vel += vect(-1, 0)
            if pressed[pg.K_RIGHT]:
                vel += vect(1, 0)
            
            vel = Normalize(vel)
            p_pos = self.player.pos
            t_size = self.world_map.tile_size
            speed_modifier = self.world_map.tiles[int(p_pos.x)//t_size][int(p_pos.y)//t_size][2]
            next_pos = p_pos + vel * speed_modifier
            
            if (0 < next_pos.x < self.world_map.width) and (0 < next_pos.y < self.world_map.height):
                self.player.move(vel, speed_modifier)

    

    def generate_world(self, w, h, tile_size=4, seed=randint(1, 500), size=1):
        self.world_map = World_map(w, h, tile_size, seed, size)
        

    def place_player(self, pos):
        self.player = Player(pos[0], pos[1])

    """
    def save_highscore(self, name):
        #Pickle database

        try:
            with open('highscore.txt', 'rb') as f:
                scores = pickle.load(f)  #score = {'Name':'','Score':0,'Stage':0} layout of stored indexes
        except:
            print('No Scorefile, creating score file')
            score = {'Name': '', 'Score': 0, 'Stage': 0}
            scores = []
            for i in range(5):
                scores.append(score)
            with open('highscore.txt', 'wb') as f:
                pickle.dump(scores, f)
        for i in range(len(scores)):
            if self.points > scores[i]['Score']:
                newHigh = {'Name': str(name), 'Score': self.points, 'Stage': self.stage}
                scores.insert(i, newHigh)
                break
        scores = scores[:5]
        self.localScores = scores[:5]
        with open('highscore.txt', 'wb') as f:
            print('saving scorefile')
            pickle.dump(scores, f)


        #online database
        if self.points > 0:
            self.logger.post_score('Astroid', self.points, str(name), self.stage)

        scores = []
        try:
            for s in self.logger.get_scores('Astroid'):
                scores.append({'Name': s['Opt1'], 'Score': s['Score'], 'Stage': s['Opt2']})
            scores = sorted(scores, key=lambda scores: scores['Score'], reverse=True)
        except:
            print('server database error')

        self.reload()

    def get_highscores(self):
        scores = []
        try:
            for s in self.logger.get_scores('Astroid'):
                scores.append({'Name': s['Opt1'], 'Score': s['Score'], 'Stage': s['Opt2']})
            return sorted(scores, key=lambda scores: scores['Score'], reverse=True)
        except:
            print('server database error')
            return []

    def get_local_highscores(self):
        try:
            with open('highscore.txt', 'rb') as f:
                scores = pickle.load(f)  #score = {'name':'','score':0,'stage':0}
        except:
            print('No Scorefile, creating score file')
            score = {'Name': '', 'Score': 0, 'Stage': 0}
            scores = []
            for i in range(5):
                scores.append(score)
            with open('highscore.txt', 'wb') as f:
                pickle.dump(scores, f)
        return scores
    """
    def start_game(self, pos):
        if self.state == 0.5:
            self.place_player(pos)
            self.state = 1

    def generate_game(self):
        if self.state == 0:
            self.state = 0.5
        
        self.generate_world(200,150,4,randint(1,500),3)
        

    def end_game(self):
        if self.state > 0:
            self.state = 0

    def toggle_pause(self):
        if self.state == 1:
            self.state = 2
            #self.scores = self.get_highscores()[:10]
        elif self.state == 2:
            self.state = 1

    """
    def highscore_input(self):
        if self.state == 1:
            self.state = 3
    """

"""
def mapFromTo(x, a, b, c, d):
    y = (x - a) / (b - a) * (d - c) + c
    return y


def uniq(lst):
    seen = set()
    uniq = []
    for x in lst:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    uniq.sort()
    return uniq
"""