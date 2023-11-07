import pygame
from tile import Tile
from settings import *
from player import Player

scale = 0.12 

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    player_sprite = Player("lib/images/game_char.png", x, y, scale)
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.vel = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_x > 0:
            self.world_shift = -8
            player.vel = 0
        else:
            self.world_shift = 0
            player.vel = 8

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.vel

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

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