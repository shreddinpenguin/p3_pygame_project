import pygame
import math
from player import *
from settings import *
from level import *
from relationships import *

def run_game():
    global run
    global globalScore
    pygame.init()
    def display_score():
        pygame.font.init()
        font = pygame.font.Font(None, 60)
        globalScore = int(pygame.time.get_ticks() / 1400)
        score_surf = font.render(str(globalScore), True, "black")
        score_rect = score_surf.get_rect(midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10))
        screen.blit(score_surf,score_rect)
        if score_surf is None:
            run = False
        print(globalScore)
        return globalScore

    #setting screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    #framerate
    FPS = 60
    pygame.display.set_caption('Flap.py')
    clock = pygame.time.Clock()
    level = Level(level_map, screen)
    points = 0

    #background load & scroll
    bg = pygame.image.load("lib/images/cloud-bg.jpeg").convert()
    bg_width = bg.get_width()
    scroll = 0
    panes = math.ceil(SCREEN_HEIGHT / bg_width) + 1
    #game loop
    run = True
    
    while run:
        #setting FPS
        clock.tick(FPS)
        #Background scroll
        for i in range(0, panes):
            screen.blit(bg, (i * bg_width + scroll, 0))
        scroll -= 0.5
        if abs(scroll) > bg_width:
            scroll = 0
        level.run()
        display_score()
        points = level.points
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    pygame.quit()
    return points
    


