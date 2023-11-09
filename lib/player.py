import pygame
from settings import SCREEN_HEIGHT
# from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.flip = False
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.vel = 5
        self.gravity = 0
        self.jump_speed = -10
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.direction.y >= -1:
            self.jump()
            self.gravity = 0.8

    def apply_gravity(self):
        if self.rect.y <= SCREEN_HEIGHT:
            self.direction.y += self.gravity
            self.rect.y += self.direction.y
        else:
            pygame.quit()
    
    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.move()
        self.rect.x += self.direction.x * self.vel