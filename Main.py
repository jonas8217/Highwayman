import pygame
import pygame_textinput
from math import sqrt
from Dist import dist
from Game import Game

def draw_game():
    screen_info = pygame.display.Info()
    w, h = screen_info.current_w, screen_info.current_h

    if game.state == 0:

        game.textinput = pygame_textinput.TextInput()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, w, h))

        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, h//2 - 20, 80, 40))
        screen.blit(small_font.render("MENU", 1, (255, 255, 255)), (381, 291))

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
        p_pos = game.player.pos # Position of player
        map = game.world_map    # World_map object
        ts = game.tile_size      # Size of an individual tile in pixels
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

        font_size = big_font.size(' ')
        for city in map.cities:
            if dist(city.pos, (p_pos.x, p_pos.y)) < sqrt((dims[0]//2)**2 + (dims[1]//2)**2) + city.size:
                darker_col = (city.color[0]-50, city.color[1]-50, city.color[2]-50)
                c_pos = world_to_screen(city.pos)
                pygame.draw.circle(screen, city.color, c_pos, city.size * S, 0)
                pygame.draw.circle(screen, darker_col, c_pos, (city.size-2) * S, 0)
                screen.blit(big_font.render(str(city.sorted_resources[0]), 1, (255, 255, 0)), (c_pos[0] - int(S * city.size/3) - font_size[0]/2, c_pos[1] - font_size[1]/2))
                screen.blit(big_font.render(str(city.sorted_resources[1]), 1, (  0, 255, 0)), (c_pos[0] + int(S * city.size/3) - font_size[0]/2, c_pos[1] - font_size[1]/2))

        for unit in game.trade_units:
            unit_pos = world_to_screen(unit.pos)
            pygame.draw.circle(screen, (0, 255, 0), unit_pos, 2 * S, 0)
            for guard in unit.guards:
                guard_pos = world_to_screen(guard.rel_pos + unit.pos)
                pygame.draw.circle(screen, (0, 0, 255), guard_pos, 2 * S, 0)
        
        # Player
        #pygame.draw.circle(screen, (255, 0, 0), (int(p_pos.x * ts), int(p_pos.y * ts)), ts//2, 0)
        pygame.draw.circle(screen, (255, 0, 0), (w//2 + S * ts//2, h//2 + S * ts//2), S * ts//2, 0)

        """
        pygame.draw.polygon(screen, (255, 255, 255), game.Ship_pointlist(), 1)
        if game.thrust_counter > 9:
            game.thrust_counter = 0
        if 0 <= game.thrust_counter <= 5 and game.thrust:
            pygame.draw.polygon(screen, (255, 255, 255), game.Ship_thrust_pointlist(), 1)
        game.thrust_counter += 1
        """

        
        # Hud
        
        screen.blit(small_font.render("Gold: {}".format(game.player.gold), 1, (0, 0, 0)), (20, 20))
        screen.blit(small_font.render("Provisions: {}".format(game.player.provisions), 1, (0, 0, 0)), (20, 35))
        #screen.blit(small_font.render("Materials: {}".format(game.player.materials), 1, (0, 0, 0)), (20, 50))
        
        # Health


    elif game.state == 2:
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, h//2 - 20, 80, 40))
        screen.blit(small_font.render("PAUSE", 1, (255, 255, 255)), (377, 291))

    if game.state == 2 or game.state == 0:
        """
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 10, 210, 40 + 15 * len(game.scores)))
        screen.blit(small_font.render("Highscores:", 1, (255, 255, 0)), (590, 20))
        for i, j in enumerate(game.scores):
            screen.blit(small_font.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 35 + i * 15))
        """
        """
        controls = ["Controls:", "Movement: WASD", "Pause: p", "Exit Game/New Game: ESC", "Sumbmit Score: Enter"]
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(260, 400, 300, 120))
        screen.blit(small_font.render("Controls:", 1, (255, 255, 255)), (270, 405))
        screen.blit(small_font.render("Movement: WASD", 1, (255, 255, 255)), (280, 420))
        screen.blit(small_font.render("Turn: Left and Right Arrows", 1, (255, 255, 255)), (280, 435))
        screen.blit(small_font.render("Shoot: Spacebar", 1, (255, 255, 255)), (280, 450))
        screen.blit(small_font.render("Pause: p", 1, (255, 255, 255)), (280, 465))
        screen.blit(small_font.render("Exit Game/New Game: ESC", 1, (255, 255, 255)), (280, 480))
        screen.blit(small_font.render("Sumbmit Score: Enter", 1, (255, 255, 255)), (280, 495))
        """
        """
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 400, 210, 30 + 15 * len(game.localScores)))
        screen.blit(small_font.render("Local Highscores:", 1, (255, 255, 0)), (590, 405))
        for i, j in enumerate(game.localScores):
            screen.blit(small_font.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 420 + i * 15))
        """

    elif game.state == 3:
        """
        screen.fill((225, 225, 225))
        screen.blit(game.textinput.get_surface(), (10, 10))
        if game.textinput.update(events) and len(game.textinput.get_text()) > 0:
            game.save_highscore(game.textinput.get_text())
        """

def screen_to_world(pos):
    return (int(pos[0]/game.tile_size), int(pos[1]/game.tile_size))


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