from math import ceil
from random import randint
from highscoreLogger import Logger
from Worldgen import World_map
from Player import Player
from Trade_unit import Trade_unit
from Vector import Normalize, Vector as vect
from Dist import dist
import pickle
from highscoreLogger import Logger
from time import time



class Game:
    def __init__(self):
        self.logger = Logger()

        self.state = 0

        self.world_map = None

        self.game_scale = 5
        self.tile_size = 4
        self.world_dim = (200,150)
        self.game_dim = (self.world_dim[0]//self.game_scale, self.world_dim[1]//self.game_scale)
        
        self.player = None

        self.trade_units = []
        

        # Reference times
        self.game_time = 0
        self.game_ref_time = time()
        self.eat_ref_time = time()
        self.merchant_spawn_ref_time = time()

        # Highscores
        self.localScores = self.get_local_highscores()[:5]


    def tick(self, pg, pressed):
        if self.state == 0.5:
            if pressed[pg.K_r]:
                self.generate_world(self.world_dim[0],self.world_dim[1],randint(1,500),3)
        
        if self.state == 1:

            # Controls input
            # Player
            p_vel = vect(0, 0)
            if pressed[pg.K_UP]:
                p_vel += vect(0, -1)
            if pressed[pg.K_DOWN]:
                p_vel += vect(0, 1)
            if pressed[pg.K_LEFT]:
                p_vel += vect(-1, 0)
            if pressed[pg.K_RIGHT]:
                p_vel += vect(1, 0)
            
            
            
            # Debugging
            if pressed[pg.K_m]:
                self.trade_units.append(Trade_unit(self.world_map.cities[0], self.world_map.cities[1], None))

            # Movement
            # Player
            p_vel = Normalize(p_vel)
            
            p_pos = self.player.pos
            ts = self.tile_size
            speed_modifier = self.world_map.tiles[int(p_pos.x)][int(p_pos.y)][2]
            
            next_pos = p_pos + p_vel * speed_modifier * self.player.speed

            # Stops player from moving outside the world
            if (0 < int(next_pos.x) < self.world_map.width) and (0 < int(next_pos.y) < self.world_map.height):
                self.player.move(p_vel, speed_modifier)

            # Trade_units
            to_pop = []
            for unit in self.trade_units:
                if dist(unit.pos, unit.end_city.pos) < 1 * ts:
                    to_pop.append(unit)
                else:
                    pos = None
                    if dist((int(p_pos.x), int(p_pos.y)), unit.pos) < unit.detect_dist:
                        pos = vect(p_pos.x, p_pos.y) 
                    unit.move(pos)
            
            for unit in to_pop[::-1]:
                self.trade_units.remove(unit)
            # Time Stuff

            self.game_time = time() - self.game_ref_time

            # Timed events
            # Player
            if time() - self.eat_ref_time > 20:
                if self.player.provisions > 0:
                    self.player.provisions -= 1
                else:
                    self.death()
                self.eat_ref_time = time()
            
            # Cities
            if time() - self.merchant_spawn_ref_time > 3: # most timings are temporary #TODO
                self.spawn_trade_unit()
                self.merchant_spawn_ref_time = time()


    def spawn_trade_unit(self):
        city_list = []
        for city in self.world_map.cities:
            for i in range(ceil(city.weight/2)):
                if (len(city.roads) > 0) and (city.weight > 0):
                    city_list.append(city)
        
        start_city = city_list[randint(0,len(city_list) - 1)]
        end_city = start_city.roads[randint(0,len(start_city.roads) - 1)]

        cargo_size = randint(1, ceil(start_city.weight/2))
        cargo = [0,0,0]
        for i in range(cargo_size):
            item = start_city.resources[randint(0,len(start_city.resources) - 1)]
            cargo[item] += 1
        
        guards = randint(0, cargo_size - 1) + randint(0, ceil(start_city.weight/2) - 1)

        self.trade_units.append(Trade_unit(start_city, end_city, cargo, guards))

    def generate_world(self, w, h, seed=randint(1, 500), size=1):
        self.world_map = World_map(w, h, seed, size)
        

    def place_player(self, pos):
        self.player = Player(pos[0], pos[1])

    
    def save_highscore(self, name):
        #Pickle database

        try:
            with open('highscore.txt', 'rb') as f:
                scores = pickle.load(f)  #score = {'Name':'','Gold':0,'Time':0} layout of stored indexes
        except:
            print('No Scorefile, creating score file')
            score = {'Name': '', 'Gold': 0, 'Time': 0}
            scores = []
            for i in range(5):
                scores.append(score)
            with open('highscore.txt', 'wb') as f:
                pickle.dump(scores, f)
        for i in range(len(scores)):
            if self.player.gold > scores[i]['Gold']:
                newHigh = {'Name': str(name), 'Gold': self.player.gold, 'Time': self.game_time}
                scores.insert(i, newHigh)
                break
        scores = scores[:5]
        self.localScores = scores[:5]
        with open('highscore.txt', 'wb') as f:
            print('saving scorefile')
            pickle.dump(scores, f)

        """
        #online database
        if self.player.gold > 0:
            self.logger.post_score('Highwayman', self.player.gold, str(name), self.game_time)

        scores = []
        try:
            for s in self.logger.get_scores('Highwayman'):
                scores.append({'Name': s['Opt1'], 'Gold': s['Gold'], 'Time': s['Opt2']})
            scores = sorted(scores, key=lambda scores: scores['Gold'], reverse=True)
        except:
            print('server database error')
        """
        self.reset()
        self.end_game()

    """
    def get_highscores(self):
        scores = []
        try:
            for s in self.logger.get_scores('Highwayman'):
                scores.append({'Name': s['Opt1'], 'Gold': s['Gold'], 'Time': s['Opt2']})
            return sorted(scores, key=lambda scores: scores['Gold'], reverse=True)
        except:
            print('server database error')
            return []
    """
    def get_local_highscores(self):
        try:
            with open('highscore.txt', 'rb') as f:
                scores = pickle.load(f)  #score = {'name':'','score':0,'Time':0}
        except:
            print('No Scorefile, creating score file')
            score = {'Name': '', 'Gold': 0, 'Time': 0}
            scores = []
            for i in range(5):
                scores.append(score)
            with open('highscore.txt', 'wb') as f:
                pickle.dump(scores, f)
        return scores
    
    def start_game(self, pos):
        if self.state == 0.5:
            self.place_player(pos)
            self.state = 1

    def generate_game(self):
        if self.state == 0:
            self.state = 0.5
        
        self.generate_world(200,150,randint(1,500),3)
        

    def end_game(self):
        if self.state > 0:
            self.state = 0

    def toggle_pause(self):
        if self.state == 1:
            self.state = 2
        elif self.state == 2:
            self.state = 1
    
    def highscore_input(self):
        if self.state == 1:
            self.state = 3

    def death(self):
        if self.state == 1:
            self.highscore_input()
    
    def reset(self):
        self.player = None
        self.trade_units[:] = []
        self.localScores = self.get_local_highscores()[:5]


    
    
    

