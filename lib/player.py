import pygame

screen = pygame.display.set_mode((800, 600))
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
        self.gravity = 0.8
        self.jump_speed = -10

    def flip_left(self):
        self.flip = True
        self.draw()

    def flip_right(self):
        self.flip = False 
        self.draw()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1 / 2
            self.flip_left()
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1 / 2
            self.flip_right()
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.move()
        self.rect.x += self.direction.x * self.vel