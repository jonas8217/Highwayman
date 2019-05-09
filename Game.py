from math import ceil, pi
from random import randint
from Worldgen import World_map
from Player import Player
from Trade_unit import Trade_unit
from Trap import Trap
from Vector import Normalize, Vector as vect
from Vector_math import vect_to_angle, vectors_to_angle, angle_to_vector
from Dist import dist
import pickle
from time import time



class Game:
    def __init__(self, screen_info):
        w, h = screen_info.current_w, screen_info.current_h
        self.state = 0

        self.world_map = None

        self.game_scale = 5
        self.tile_size = 4
        self.world_dim = (w//self.tile_size,h//self.tile_size)
        self.game_dim = (self.world_dim[0]//self.game_scale, self.world_dim[1]//self.game_scale)
        
        self.player = None

        self.trade_units = []

        self.player_traps = []
        

        # Reference times
        self.game_time = 0
        self.game_ref = time()
        self.eat_ref = time()
        self.regen_ref = time()
        self.attack_ref = time()
        self.place_trap_ref = time()
        self.merchant_spawn_ref = time()

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
            if pressed[pg.K_SPACE]:
                attack = True
            else:
                attack = False
            if pressed[pg.K_t]:
                place_trap = True
            else:
                place_trap = False
            
            
            # Player actions
            if place_trap:
                if time() - self.place_trap_ref > 0.2:
                    if self.player.materials >= 5:
                        self.place_trap_ref = time()
                        self.player.materials -= 5
                        self.player_traps.append(Trap((int(self.player.pos[0]), int(self.player.pos[1]))))
    
            # Movement
            # Player
            p_vel = Normalize(p_vel)
            
            
            p_pos = vect(self.player.pos.x, self.player.pos.y)

            speed_modifier = self.world_map.tiles[int(p_pos.x)][int(p_pos.y)][2]
            
            next_pos = p_pos + p_vel * speed_modifier * self.player.speed

            # Stops player from moving outside the world
            if (0 < next_pos.x < self.world_map.width) and (0 < next_pos.y < self.world_map.height):
                self.player.move(p_vel, speed_modifier)

            # Trade_units
            to_pop = []
            for unit in self.trade_units:
                if dist(unit.pos, unit.end_city.pos) < 1 * unit.end_city.size / self.tile_size:
                    to_pop.append(unit)
                else:
                    player = None
                    if dist((int(p_pos.x), int(p_pos.y)), unit.pos) < unit.detect_dist:
                        player = self.player
                    unit.move(player)
            
            for unit in to_pop[::-1]:
                self.trade_units.remove(unit)

            # Attacks
            # Player
            
            if attack:
                if time() - self.player.last_attacked > self.player.attack_rate:
                    self.player.last_attacked = time()
                    for unit in self.trade_units:
                        if dist(unit.pos, self.player.pos) < self.player.attack_range:
                            if abs(vectors_to_angle(unit.pos - self.player.pos, angle_to_vector(self.player.rotation))) < pi/3:
                                self.player.attack(unit)
                                self.check_if_unit_dead(unit)
                        for guard in unit.guards:
                            if dist(guard.rel_pos + unit.pos, self.player.pos) < self.player.attack_range:
                                if abs(vectors_to_angle((guard.rel_pos + unit.pos) - self.player.pos, angle_to_vector(self.player.rotation))) < pi/3:
                                    self.player.attack(guard)
                                    unit.check_if_guard_dead(guard)
            

            # Guards
            for unit in self.trade_units:
                for guard in unit.guards:
                    pos = unit.pos + guard.rel_pos
                    if dist(pos, p_pos) < guard.attack_range:
                        if time() - guard.last_attacked > guard.attack_rate:
                            guard.last_attacked = time()
                            guard.attack(self.player)
                            self.check_if_player_dead()

            # Traps
            for trap in self.player_traps:
                for unit in self.trade_units:
                    if dist(trap.pos, unit.pos) < 1:
                        trap.attack(unit)
                        self.player_traps.remove(trap)
                        self.check_if_unit_dead(unit)
                        break
                    for guard in unit.guards:
                        if dist(trap.pos, (guard.rel_pos + unit.pos)) < 1:
                            trap.attack(guard)
                            self.player_traps.remove(trap)
                            unit.check_if_guard_dead(guard)
                            break
                    else:
                        continue
                    break





            # Time Stuff

            self.game_time = time() - self.game_ref

            # Timed events
            # Player
            if time() - self.eat_ref > 25 - (self.player.max_hp - self.player.hit_points): # Eating
                if self.player.provisions > 0:
                    self.player.provisions -= 1
                else:
                    self.death()
                self.eat_ref = time()

            if time() - self.regen_ref > 1.75:
                if self.player.hit_points < self.player.max_hp:
                    self.player.hit_points += 1
                    self.regen_ref = time()

            
            
            # Cities
            if time() - self.merchant_spawn_ref > 3:
                self.spawn_trade_unit()
                self.merchant_spawn_ref = time()


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

        self.trade_units.append(Trade_unit(start_city, end_city, cargo, time(), guards))

    def check_if_unit_dead(self, unit):
        if unit.hit_points <= 0:
            self.player.gold += unit.cargo[0] * randint(5,10)
            self.player.provisions += unit.cargo[1] * randint(5,10)
            self.player.materials += unit.cargo[2] * randint(5,10)
            self.trade_units.remove(unit)

    def check_if_player_dead(self):
        if self.player.hit_points <= 0:
            self.death()


    def generate_world(self, w, h, seed=randint(1, 500), size=1):
        self.world_map = World_map(w, h, seed, size)
        

    def place_player(self, pos):
        self.player = Player(pos[0], pos[1], time())

    
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
        
        self.generate_world(self.world_dim[0],self.world_dim[1],randint(1,500),3)
        

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
