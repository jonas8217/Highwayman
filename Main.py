import pygame
import pygame_textinput
from math import sqrt
from Game import Game

def draw_game():
    screen_info = pygame.display.Info()
    w, h = screen_info.current_w, screen_info.current_h

    if game.state == 0:

        game.textinput = pygame_textinput.TextInput()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, w, h))

        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, h//2 - 20, 80, 40))
        screen.blit(myfont.render("MENU", 1, (255, 255, 255)), (381, 291))

    elif game.state == 0.5:

        map = game.world_map # World_map object
        ts = map.tile_size # size of an individual tile in pixels

        screen.fill((255, 255, 255))
        for x in range(map.width):
            for y in range(map.height):
                pygame.draw.rect(screen, map.tiles[x][y][1], pygame.Rect(x * ts, y * ts, ts, ts))
        for road in map.roads:
            pygame.draw.line(screen, (181, 103, 36), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), 5)
            pygame.draw.line(screen, (209, 147, 54), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), 3)
        for city in map.cities:
            pygame.draw.circle(screen, city.col, (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size, 0)
            pygame.draw.circle(screen, (city.col[0]-50, city.col[1]-50, city.col[2]-50), (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size-2, 0)
        
        
    
    elif game.state == 1:
        
        p_pos = game.player.pos # position of player
        map = game.world_map # World_map object
        ts = map.tile_size # size of an individual tile in pixels
        dims = game.game_dim # game_dim[0],game_dim[1] = game view size in tiles

        lB = 0 #leftBoundary
        rB = 0 #rightBoundary
        tB = 0 #topBoundary
        bB = 0 #bottomBoundary

        
        if int(p_pos.x)//ts - dims[0]//2 < 0:
            lB = dims[0]//2 - int(p_pos.x)//ts
        if int(p_pos.x)//ts + dims[0]//2 > map.width:
            rB = int(p_pos.x)//ts + dims[0]//2 - map.width
        if int(p_pos.y)//ts - dims[1]//2 < 0:
            tB = dims[1]//2 - int(p_pos.y)//ts
        if int(p_pos.y)//ts + dims[1]//2 > map.height:
            bB = int(p_pos.y)//ts + dims[1]//2 - map.height
        
        screen.fill((100, 100, 100))

        for x in range(int(p_pos.x)//ts - dims[0]//2 + lB, int(p_pos.x)//ts + dims[0]//2 - rB):
            for y in range(int(p_pos.y)//ts - dims[1]//2 + tB, int(p_pos.y)//ts + dims[1]//2 - bB):
                pygame.draw.rect(screen, map.tiles[x][y][1], pygame.Rect(x * ts, y * ts, ts, ts))
        for road in map.roads:
            P1, P2 = road.P1, road.P2
            roadlen = dist(P1, P2)
            PMid = ((P1[0] + P2[0])/2, (P1[1] + P2[1])/2)
            if dist(PMid, (p_pos[0]//ts, p_pos[1]//ts)) < sqrt((dims[0]//2)**2 + (dims[1]//2)**2) + roadlen/2:
                pygame.draw.line(screen, (181, 103, 36), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), 5)
                pygame.draw.line(screen, (209, 147, 54), (road.P1[0] * ts + ts/2, road.P1[1] * ts + ts/2), (road.P2[0] * ts + ts/2, road.P2[1] * ts + ts/2), 3)
        for city in map.cities:
            if sqrt(((city.pos[0] - p_pos[0]//ts)**2) + ((city.pos[1] - p_pos[1]//ts)**2)) < sqrt((dims[0]//2)**2 + (dims[1]//2)) + city.size:
                pygame.draw.circle(screen, city.col, (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size, 0)
                pygame.draw.circle(screen, (city.col[0]-50, city.col[1]-50, city.col[2]-50), (city.pos[0] * ts + ts//2 , city.pos[1] * ts + ts//2), city.size-2, 0)


        pygame.draw.circle(screen, (255, 0, 0), (int(p_pos.x), int(p_pos.y)), game.world_map.tile_size, 0)
        """
        pygame.draw.polygon(screen, (255, 255, 255), game.Ship_pointlist(), 1)
        if game.thrust_counter > 9:
            game.thrust_counter = 0
        if 0 <= game.thrust_counter <= 5 and game.thrust:
            pygame.draw.polygon(screen, (255, 255, 255), game.Ship_thrust_pointlist(), 1)
        game.thrust_counter += 1
        """

        """
        if len(game.astr) > 0:
            for i in range(len(game.astr)):
                pygame.draw.circle(screen, (255, 255, 255), (int(game.astr[i].x), int(game.astr[i].y)), game.astr[i].size * 10, 2)
        if len(game.pjct) > 0:
            for i in range(len(game.pjct)):
                pygame.draw.circle(screen, (255, 255, 255), (int(game.pjct[i].x), int(game.pjct[i].y)), 2, 0)
        """
        """
        screen.blit(myfont.render("Points: {}".format(game.points), 1, (255, 255, 0)), (20, 20))
        screen.blit(myfont.render("Shield: {}".format(game.shield), 1, (255, 255, 0)), (20, 35))
        screen.blit(myfont.render("Stage: {}".format(game.stage), 1, (255, 255, 0)), (20, 50))
        """

    elif game.state == 2:
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(w//2 - 40, h//2 - 20, 80, 40))
        screen.blit(myfont.render("PAUSE", 1, (255, 255, 255)), (377, 291))

    if game.state == 2 or game.state == 0:
        """
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 10, 210, 40 + 15 * len(game.scores)))
        screen.blit(myfont.render("Highscores:", 1, (255, 255, 0)), (590, 20))
        for i, j in enumerate(game.scores):
            screen.blit(myfont.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 35 + i * 15))
        """
        """
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(260, 400, 300, 120))
        screen.blit(myfont.render("Controls:", 1, (255, 255, 255)), (270, 405))
        screen.blit(myfont.render("Thrust: Up Arrow", 1, (255, 255, 255)), (280, 420))
        screen.blit(myfont.render("Turn: Left and Right Arrows", 1, (255, 255, 255)), (280, 435))
        screen.blit(myfont.render("Shoot: Spacebar", 1, (255, 255, 255)), (280, 450))
        screen.blit(myfont.render("Pause: p", 1, (255, 255, 255)), (280, 465))
        screen.blit(myfont.render("Exit Game/New Game: ESC", 1, (255, 255, 255)), (280, 480))
        screen.blit(myfont.render("Sumbmit Score: Enter", 1, (255, 255, 255)), (280, 495))
        """
        """
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(570, 400, 210, 30 + 15 * len(game.localScores)))
        screen.blit(myfont.render("Local Highscores:", 1, (255, 255, 0)), (590, 405))
        for i, j in enumerate(game.localScores):
            screen.blit(myfont.render(str(j['Name']) + ': ' + str(j['Score']) + ' at ' + str(j['Stage']), 1, (255, 255, 0)), (590, 420 + i * 15))
        """

    elif game.state == 3:
        """
        screen.fill((225, 225, 225))
        screen.blit(game.textinput.get_surface(), (10, 10))
        if game.textinput.update(events) and len(game.textinput.get_text()) > 0:
            game.save_highscore(game.textinput.get_text())
        """

def dist(P1,P2):
    return sqrt(((P1[0] - P2[0])**2) + ((P1[1] - P2[1])**2))

pygame.init()
"""
icon = ""
icon = io.BytesIO(base64.b64decode(icon))
icon = pygame.image.load(icon)
pygame.display.set_icon(icon)
"""
pygame.display.set_caption('highwayman')
screen = pygame.display.set_mode((800, 600))
# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

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
                game.start_game(pos)
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