import pygame

import const


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, image_path):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(const.WHITE)
        self.image.set_colorkey(const.WHITE)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def moveRight(self, player_ms):
        self.rect.x += player_ms

    def moveLeft(self, player_ms):
        self.rect.x -= player_ms

    def moveUp(self, player_ms):
        self.rect.y -= player_ms

    def moveDown(self, player_ms):
        self.rect.y += player_ms


class Arrow(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
