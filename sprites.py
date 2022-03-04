from random import randint

import pygame

import const


class Player(pygame.sprite.Sprite):
    def __init__(self, color: tuple, width: int, height: int, image_path: str):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.image.set_colorkey(color)
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
        self.x0 = x
        self.y = y
        self.y0 = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        self.weight = 0.5
        self.gravity = self.weight * 9.8
        self.time = const.TIME_UNIT

    def gravity_work(self):
        self.y = self.y0 + self.gravity * self.time ** 2 / 2


class Opponent(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, resistance: int, speed: float):
        super().__init__()

        self.color = const.BLACK
        self.image = pygame.Surface([width, height])
        self.speed = speed

        self.image.fill(self.color)
        self.image.set_colorkey(self.color)
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

        self.image_path = const.OPPONENT_SPRITE_IMAGE_PATH
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.resistance = resistance

        self.rect.x = const.WINDOW_WIDTH - 200
        self.rect.y = randint(const.WINDOW_PADDING, const.WINDOW_HEIGHT - const.WINDOW_PADDING)

    def move_towards_player(self, player_rect, speed: int):
        if self.rect.x < player_rect.x:
            self.rect.x += speed

        if self.rect.x > player_rect.x:
            self.rect.x -= speed

        if self.rect.y < player_rect.y:
            self.rect.y += speed

        if self.rect.y > player_rect.y:
            self.rect.y -= speed

    def get_hit(self):
        self.resistance -= 1
