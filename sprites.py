from random import randint

import pygame
from pygame.sprite import Group

import const
from rules import resize_image


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
    def __init__(self, x: int, y: int, radius: int, color: tuple, facing: float):
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
        self.hit = False

    def gravity_work(self):
        self.y = self.y0 + self.gravity * self.time ** 2 / 2

    def check_hit(self, opponents_group: Group):
        opponent_sprites = opponents_group.sprites()

        for opponent in opponent_sprites:
            opponent: Opponent

            if int(self.x) in range(opponent.rect.x, opponent.rect.x + opponent.rect.width) \
                    and int(self.y) in range(opponent.rect.y, opponent.rect.y + opponent.rect.height) \
                    and not self.hit:
                opponent.get_hit()
                self.hit = True


class Opponent(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, resistance: int, speed: float):
        super().__init__()

        self.color = const.BLACK
        self.image = pygame.Surface([width, height])
        self.speed = speed
        self.resistance = resistance

        self.image.fill(self.color)
        self.image.set_colorkey(self.color)
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

        self.image_path = const.OPPONENT_SPRITE_IMAGE_PATH
        resized_image_path = resize_image(self.image_path, width, height)
        self.image = pygame.image.load(resized_image_path)

        self.rect = self.image.get_rect()
        self.rect.x = const.WINDOW_WIDTH - 200
        self.rect.y = randint(const.WINDOW_PADDING, const.WINDOW_HEIGHT - const.WINDOW_PADDING)

    def move_towards_player(self, player_rect: pygame.rect, speed: int):
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

        if self.resistance <= 0:
            ...  # TODO:
