import pygame
import pygame_textinput
from math import sqrt, cos, sin, pi
from Dist import dist
from Game import Game



def draw_game():
    screen_info = pygame.display.Info()
    w, h = screen_info.current_w, screen_info.current_h
    Big_size = big_font.size(' ')
    Small_size = small_font.size(' ')
    
    if game.state == 0:

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, w, h))

        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, 50, 80, 40))
        txt_size = small_font.size("MENU")
        screen.blit(small_font.render("MENU", 1, (255, 255, 255)), (w//2 - txt_size[0]//2, 70 - txt_size[1]//2))

    elif game.state == 0.5:

        map = game.world_map # World_map object
        ts = game.tile_size # size of an individual tile in pixels

        screen.fill((255, 255, 255))
        for x in range(map.width):
            for y in range(map.height):
                pygame.draw.rect(screen, map.tiles[x][y][1], pygame.Rect(x * ts, y * ts, ts, ts))
        for road in map.roads:
            pygame.draw.line(screen, (181, 103, 36), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), int(ts * 2))
            pygame.draw.line(screen, (209, 147, 54), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), ts)
        for city in map.cities:
            pygame.draw.circle(screen, city.color, (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size, 0)
            pygame.draw.circle(screen, (city.color[0]-50, city.color[1]-50, city.color[2]-50), (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size-2, 0)
        
        
    
    elif game.state == 1:
        screen.fill((100, 100, 100))
        
        # Declaring shorter variabels for later use
        player = game.player    # Player object
        p_pos = player.pos      # Position of player
        map = game.world_map    # World_map object
        ts = game.tile_size     # Size of an individual tile in pixels
        dims = game.game_dim    # Game_dim[0],game_dim[1] = game view size in tiles
        S = game.game_scale     # Difference in scale between world and view size

        world_to_screen = lambda pos : (int(((pos[0] - p_pos.x + dims[0]//2) * ts + ts//2) * S), int(((pos[1] - p_pos.y + dims[1]//2) * ts + ts//2) * S))

        lB = 0 # LeftBoundary
        rB = 0 # RightBoundary
        tB = 0 # TopBoundary
        bB = 0 # BottomBoundary

        # Veiw boundaries
        if int(p_pos.x) - dims[0]//2 < 0:
            lB = dims[0]//2 - int(p_pos.x)
        if int(p_pos.x) + dims[0]//2 > map.width:
            rB = int(p_pos.x) + dims[0]//2 - map.width
        if int(p_pos.y) - dims[1]//2 < 0:
            tB = dims[1]//2 - int(p_pos.y)
        if int(p_pos.y) + dims[1]//2 > map.height:
            bB = int(p_pos.y) + dims[1]//2 - map.height
        

        # Rendering
        # Map
        for x in range(lB, w//(ts*S) - rB):
            for y in range(tB, h//(ts*S) - bB):
                pygame.draw.rect(screen, map.tiles[int(p_pos.x) - dims[0]//2 + x][int(p_pos.y) - dims[1]//2 + y][1], pygame.Rect(x * ts * S, y * ts  * S, ts * S, ts * S))
        
        # Roads
        for road in map.roads:
            P1, P2 = road.P1, road.P2
            roadlen = dist(P1, P2)
            PMid = ((P1[0] + P2[0])/2, (P1[1] + P2[1])/2)
            if dist(PMid, (p_pos.x, p_pos.y)) < sqrt((dims[0]//2)**2 + (dims[1]//2)**2) + roadlen/2:
                RP1_pos,RP2_pos  = world_to_screen(road.P1), world_to_screen(road.P2)
                pygame.draw.line(screen, (181, 103, 36), RP1_pos, RP2_pos, ts * S)
                pygame.draw.line(screen, (209, 147, 54), RP1_pos, RP2_pos, int(ts * S/2))

        
        for city in map.cities:
            if dist(city.pos, (p_pos.x, p_pos.y)) < sqrt((dims[0]//2)**2 + (dims[1]//2)**2) + city.size:
                darker_col = (city.color[0]-50, city.color[1]-50, city.color[2]-50)
                c_pos = world_to_screen(city.pos)
                pygame.draw.circle(screen, city.color, c_pos, city.size * S, 0)
                pygame.draw.circle(screen, darker_col, c_pos, (city.size-2) * S, 0)
                screen.blit(big_font.render(str(city.sorted_resources[0]), 1, (255, 255, 0)), (c_pos[0] - int(S * city.size/3) - Big_size[0]/2, c_pos[1] - Big_size[1]/2))
                screen.blit(big_font.render(str(city.sorted_resources[1]), 1, (  0, 255, 0)), (c_pos[0] + int(S * city.size/3) - Big_size[0]/2, c_pos[1] - Big_size[1]/2))

        for unit in game.trade_units:
            unit_pos = world_to_screen(unit.pos)
            pygame.draw.circle(screen, (0, 255, 0), unit_pos, 2 * S, 0)
            for guard in unit.guards:
                guard_pos = world_to_screen(guard.rel_pos + unit.pos)
                pygame.draw.circle(screen, (0, 0, 255), guard_pos, 2 * S, 0)
        
        # Player
        pygame.draw.circle(screen, (255, 0, 0), (w//2 + S * ts//2, h//2 + S * ts//2), S * ts//2, 0)
        p_rot = player.rotation
        pygame.draw.circle(screen, (255, 255, 255), (int(w//2 + S * ts//2 + cos(p_rot - pi/6) * S * ts//3), int(h//2 + S * ts//2 + sin(p_rot - pi/6) * S * ts//3)), int(S * ts//6), 0)
        pygame.draw.circle(screen, (255, 255, 255), (int(w//2 + S * ts//2 + cos(p_rot + pi/6) * S * ts//3), int(h//2 + S * ts//2 + sin(p_rot + pi/6) * S * ts//3)), int(S * ts//6), 0)

        
        # Hud
        
        screen.blit(small_font.render("Gold: {}".format(game.player.gold), 1, (0, 0, 0)), (20, 20))
        screen.blit(small_font.render("Provisions: {}".format(game.player.provisions), 1, (0, 0, 0)), (20, 35))
        #screen.blit(small_font.render("Materials: {}".format(game.player.materials), 1, (0, 0, 0)), (20, 50))
        
        # Health


    elif game.state == 2:
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, h//2 - 20, 80, 40))
        screen.blit(small_font.render("PAUSE", 1, (255, 255, 255)), (377, 291))

    if game.state == 2 or game.state == 0:
        
        controls = ["Movement: WASD", "Attack: Spacebar", "Pause: p", "Exit Game/New Game: ESC", "Sumbmit Score: Enter"]
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 150, 400, 300, (len(controls) + 1) * (Small_size[1] + 3) + 3))
        screen.blit(small_font.render("Controls:", 1, (255, 255, 255)), (270, 403))
        for i, text in enumerate(controls):
            screen.blit(small_font.render(text, 1, (255, 255, 255)), (275, 403 + (i + 1) * (Small_size[1] + 3)))
        
        
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 175, 120, 350, 3 + Small_size[1] + 3 + (Small_size[1] + 3) * len(game.localScores)))
        screen.blit(small_font.render("Highscores:", 1, (255, 255, 255)), (w//2 - 175 + 5, 120 + 3))
        for i, score in enumerate(game.localScores):
            if len(score['Name']) > 0:
                screen.blit(small_font.render(str(score['Name']) + ' - Gold: ' + str(score['Gold']) + ' Time: ' + str(int(score['Time']/60)) + ':' + str(int(score['Time'] % 60)), 1, (255, 255, 255)), (w//2 - 175 + 5, 120 + (i + 1) * (Small_size[1] + 3)))
        

    elif game.state == 3:
        
        screen.fill((225, 225, 225))
        screen.blit(textinput.get_surface(), (10, 10))
        if textinput.update(events) and len(textinput.get_text()) > 0:
            game.save_highscore(textinput.get_text())
        

def screen_to_world(pos):
    return (int(pos[0]/game.tile_size), int(pos[1]/game.tile_size))

def pixel(color, pos):
    screen.fill(color, (pos, (1, 1)))


pygame.init()
"""
icon = ""
icon = io.BytesIO(base64.b64decode(icon))
icon = pygame.image.load(icon)
pygame.display.set_icon(icon)
"""
pygame.display.set_caption('highwayman')
screen = pygame.display.set_mode((800, 600))
# Initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
small_font = pygame.font.SysFont("monospace", 15)
big_font = pygame.font.SysFont("monospace", 45)
textinput = pygame_textinput.TextInput()

running = True

game = Game()

clock = pygame.time.Clock()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if game.state == 1 or game.state == 2:
                game.toggle_pause()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.state == 0.5:
                pos = pygame.mouse.get_pos()
                game.start_game(screen_to_world(pos))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game.state != 0:
                game.end_game()
            else:
                game.generate_game()

    pressed = pygame.key.get_pressed()

    game.tick(pygame, pressed)

    draw_game()
    pygame.display.flip()
    clock.tick(60)