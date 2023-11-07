import pygame
import math
from sys import exit
from player import *
import random
from settings import *
from tile import Tile
from level import *

pygame.init()
#setting screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
#character starting coordinates
enemy_x = random.randint(1, 600)
enemy_y = 510 
FPS = 60
dimension = 30
pygame.display.set_caption('PyGuy')
clock = pygame.time.Clock()
level = Level(level_map, screen)
is_jump = False 
jump_count = 10

#background load & scroll
bg = pygame.image.load("lib/images/cloud-bg.jpeg").convert()
bg_width = bg.get_width()
scroll = 0
panes = math.ceil(SCREEN_HEIGHT / bg_width) + 1

#game loop
while True:
    #setting FPS
    clock.tick(FPS)
    #Background scroll
    for i in range(0, panes):
        screen.blit(bg, (i * bg_width + scroll, 0))
    scroll -= 0.5
    if abs(scroll) > bg_width:
        scroll = 0
    level.run()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    
