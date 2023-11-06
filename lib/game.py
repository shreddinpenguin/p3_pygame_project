import pygame
import math
from sys import exit
from char_class import Character
import random

pygame.init()
#window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
#character starting coordinates
enemy_x = random.randint(1, 600)
enemy_y = 510
stx = 50
sty = 510
scale = 0.12
vel = 5
FPS = 60
dimension = 30
pygame.display.set_caption('PyGuy')
clock = pygame.time.Clock()
floor = pygame.Surface((800, 50))
floor.fill('Green')
is_jump = False 
jump_count = 10

#background load & scroll
bg = pygame.image.load("cloud-bg.jpeg").convert()
bg_width = bg.get_width()
scroll = 0
tiles = math.ceil(SCREEN_HEIGHT / bg_width) + 1

#game loop
while True:
    #setting FPS
    clock.tick(FPS)
    #Background scroll
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
    scroll -= 0.5
    if abs(scroll) > bg_width:
        scroll = 0
   #Game character
    player = Character("game_char.png", stx, sty, scale, vel)
    enemy = Character("goblin.png", enemy_x, enemy_y, 0.15, vel)
    player.draw()
    enemy.draw()
    # enemy.move()
    screen.blit(floor, (0,550))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and stx > dimension:
        player.flip_left()
        stx -= vel
        # player.direction = -1
    elif keys[pygame.K_RIGHT] and stx < SCREEN_WIDTH - dimension:
        stx += vel
        player.flip_right()
        player.direction = 1
    #jumping logic
    if not (is_jump): 
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count  < 0:
                neg = -1
            sty -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10

    pygame.display.update()
    
