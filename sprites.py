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
        self.points = 0  # killed_opponents
        self.health = 100

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
        self.vel = 28 * facing
        self.weight = 0.5
        self.gravity = self.weight * 9.8
        self.time = const.TIME_UNIT
        self.hit = False

    def gravity_work(self):
        self.y = self.y0 + self.gravity * self.time ** 2 / 2

    def check_hit(self, opponents_group: Group, player_sprite: Player):
        opponent_sprites = opponents_group.sprites()

        for opponent in opponent_sprites:
            opponent: Opponent

            if int(self.x) in range(opponent.rect.x, opponent.rect.x + opponent.rect.width) \
                    and int(self.y) in range(opponent.rect.y, opponent.rect.y + opponent.rect.height) \
                    and not self.hit:
                killed = opponent.get_hit()
                self.hit = True

                if killed:
                    player_sprite.points += 1


class Opponent(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, resistance: int, speed: float):
        super().__init__()

        self.color = const.BLACK
        self.hit_color = const.RED

        self.surface = pygame.Surface([width, height])
        self.speed = speed
        self.resistance = resistance

        self.surface.fill(self.color)
        self.surface.set_colorkey(self.color)
        pygame.draw.rect(self.surface, self.color, [0, 0, width, height])

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

        if self.rect.y < player_rect.y + player_rect.height / 2.5:
            self.rect.y += speed

        if self.rect.y > player_rect.y + player_rect.height / 2.5:
            self.rect.y -= speed

    def get_hit(self) -> bool:
        killed = False

        self.resistance -= 1

        if self.resistance <= 0:
            self.kill()

            killed = True

        return killed

    def attack_player(self, player_sprite: Player, counter: int) -> bool:
        killed = False

        if self.rect.colliderect(player_sprite) and counter % 10 == 0:  # % 10 to slow down taking life
            player_sprite.health -= 1

            if player_sprite.health <= 0:
                player_sprite.kill()

                return killed
