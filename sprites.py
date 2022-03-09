from random import randint

from pygame import rect, Surface
from pygame.image import load
from pygame.sprite import Group, Sprite

import const
from rules import resize_image


class Player(Sprite):
    def __init__(self, image_path: str, x=0, y=0):
        super().__init__()
        self.image = load(image_path)

        self.points = 0  # killed_opponents
        self.health = 100

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.vel = 14 * facing
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


class Opponent(Sprite):
    def __init__(self, width: int, height: int, resistance: int, speed: float):
        super().__init__()

        self.color = const.BLACK
        self.hit_color = const.RED

        self.surface = Surface([width, height])
        self.speed = speed
        self.resistance = resistance

        self.image_path = const.OPPONENT_SPRITE_IMAGE_PATH
        resized_image_path = resize_image(self.image_path, width, height)
        self.image = load(resized_image_path)

        self.rect = self.image.get_rect()
        self.rect.x = randint(const.WINDOW_WIDTH - 400, const.WINDOW_WIDTH - 200)
        self.rect.y = randint(const.WINDOW_PADDING, const.WINDOW_HEIGHT - const.WINDOW_PADDING)

    def move_towards_player(self, player_rect: rect):
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed

        if self.rect.x > player_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player_rect.y + player_rect.height / 2.5:
            self.rect.y += self.speed

        if self.rect.y > player_rect.y + player_rect.height / 2.5:
            self.rect.y -= self.speed

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


class ShopIcon(Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = load(const.SHOP_ICON_IMAGE_PATH)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class ShopContainer(Sprite):
    def __init__(self, screen: Surface, color=const.ORANGE):
        super().__init__()

        self.image = screen

        self.image.fill(color)
        self.image.set_colorkey(color)

        self.rect = self.image.get_rect()


class ShopItem(Sprite):
    def __init__(self, image_path, item_pos: dict):
        super().__init__()

        self.image = load(image_path)
        self.rect = self.image.get_rect()

        self.rect.x = item_pos['x']
        self.rect.y = item_pos['y']




