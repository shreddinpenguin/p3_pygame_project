import pygame
from tile import Tile
from settings import *
from player import Player
scale = 0.16  
start_score = False
globalScore = 0
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        # self.points = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for y_offset in range(10):
            for row_index, row in enumerate(layout):
                for x_offset in range(10):
                    for col_index, cell in enumerate(row):
                        if cell == 'X':
                            x = col_index * tile_size + x_offset * (len(row) * tile_size)
                            y = row_index * tile_size + y_offset * (len(layout) * tile_size)
                            tile = Tile((x,y), tile_size)
                            self.tiles.add(tile)
                        if cell == 'P':
                            x = col_index * tile_size
                            y = row_index * tile_size
                            player_sprite = Player("lib/images/crop_bird.png", x, y, scale)
                            self.player.add(player_sprite)

    def scroll_x(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.world_shift = -4
    
    def display_score(self):
        self.font = pygame.font.SysFont('Arial', 40)
        globalScore = int(pygame.time.get_ticks() // 1400)
        score_surf = self.font.render(str(self.points), True, "black")
        score_rect = score_surf.get_rect(midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10))
        self.display_surface.blit(score_surf,score_rect)
        return globalScore

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.vel

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    pygame.quit()
                    return self.points
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    pygame.quit()
                    return self.points

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    pygame.quit()
                    return self.points
                elif SCREEN_HEIGHT <= player.direction[1]:
                    pygame.quit()
                    return self.points
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    pygame.quit()
                    return self.points

    def run(self):
        #level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        #player
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()
        self.display_score()
