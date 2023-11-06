import pygame

screen = pygame.display.set_mode((800, 600))
class Character(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scale, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.vel = vel
        self.direction = 1
        self.flip = False
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def move(self):
        x -= self.vel

    def flip_left(self):
        self.flip = True
        self.draw()

    def flip_right(self):
        self.flip = False 
        # self.draw()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)