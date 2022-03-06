import os
import sys
from random import randint

import pygame
from pygame.locals import *

import const
import sprites

pygame.init()

# fonts
monospace_12 = pygame.font.SysFont(*const.monospace_12)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s, %s' % (const.WINDOW_POSITION_X, const.WINDOW_POSITION_Y)

fps = 60
fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode(const.WINDOW_SIZE)
pygame.display.set_caption('pygame player vs opponents shooting game')

player_sprite = sprites.Player(const.BLACK, 30, 40, const.PLAYER_SPRITE_IMAGE_PATH)
player_sprite.rect.x, player_sprite.rect.y = const.INIT_PLAYER_X, const.INIT_PLAYER_Y

arrows = []
facing = 1

player_group = pygame.sprite.Group(player_sprite)
opponents_group = pygame.sprite.Group()

pygame.display.update()

main_loop_counter = 0
game_started = True


def show_points(points: int):
    points_label = monospace_12.render('Points: %d' % points, True, const.ORANGE)

    screen.blit(points_label, (
        const.WINDOW_WIDTH - const.WINDOW_PADDING - (const.WINDOW_WIDTH * 0.05),  # x
        const.WINDOW_HEIGHT * 0.025  # y
    ))


def show_player_health(health: int):
    health_label = monospace_12.render('Health: %d' % health, True, const.DARK_GREEN)

    screen.blit(health_label, (
        const.WINDOW_WIDTH - const.WINDOW_PADDING - (const.WINDOW_WIDTH * 0.055),  # x
        const.WINDOW_HEIGHT * 0.05  # y
    ))


def show_shop_label():
    shop_icon_img = pygame.image.load(const.SHOP_ICON_IMAGE_PATH)

    screen.blit(shop_icon_img, (
            const.WINDOW_WIDTH * 0.025,
            const.WINDOW_HEIGHT * 0.01
    ))


while True:
    main_loop_counter += 1

    screen.fill(const.WHITE)
    key_pressed = pygame.key.get_pressed()
    player_rect = player_group.sprites()[0].rect

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if key_pressed[pygame.K_ESCAPE]:
        break

    if (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]) \
            and player_sprite.rect.left > const.WINDOW_PADDING:
        player_sprite.moveLeft(const.PLAYER_SPEED)

    if (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) \
            and player_sprite.rect.right < (const.WINDOW_WIDTH - const.WINDOW_PADDING):
        player_sprite.moveRight(const.PLAYER_SPEED)

    if (key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]) \
            and player_sprite.rect.bottom < (const.WINDOW_HEIGHT - const.WINDOW_PADDING):
        player_sprite.moveDown(const.PLAYER_SPEED)

    if (key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]) \
            and player_sprite.rect.top > const.WINDOW_PADDING:
        player_sprite.moveUp(const.PLAYER_SPEED)

    if key_pressed[pygame.K_SPACE] and player_sprite.rect.left:  # right click
        facing = -1
    elif key_pressed[pygame.K_SPACE] and not player_sprite.rect.left:
        facing = 1

    if key_pressed[pygame.K_SPACE] and len(arrows) < const.MAX_ARROWS_COUNT:
        if arrows and arrows[-1].time > 1:
            arrows.append(
                sprites.Arrow(
                    round(player_sprite.rect.x + player_sprite.rect.width // 2),
                    round(player_sprite.rect.y + player_sprite.rect.height // 2), 6, const.RED, facing
                )
            )
        elif not arrows:
            arrows.append(
                sprites.Arrow(
                    round(player_sprite.rect.x + player_sprite.rect.width // 2),
                    round(player_sprite.rect.y + player_sprite.rect.height // 2), 6, const.RED, facing
                )
            )
        else:
            pass

    if len(opponents_group) < 2:
        opponent_sprite = sprites.Opponent(
            width=const.OPPONENT_WIDTH,
            height=const.OPPONENT_HEIGHT,
            resistance=randint(1, 8),
            speed=1
        )

        opponents_group.add(opponent_sprite)

    for arrow in arrows:
        arrow.time += const.TIME_UNIT

        if arrow.x < const.WINDOW_WIDTH > 0 and arrow.y < const.WINDOW_HEIGHT > 0:
            arrow.x -= arrow.vel
            # arrow.gravity_work()
        else:
            arrows.remove(arrow)

    for arrow in arrows:  # type: sprites.Arrow
        pygame.draw.circle(screen, arrow.color, (arrow.x, arrow.y), arrow.radius)
        arrow.check_hit(opponents_group, player_sprite)

    for opponent in opponents_group:
        opponent: sprites.Opponent
        opponent.move_towards_player(player_rect, 1)
        opponent.attack_player(player_sprite, main_loop_counter)

    show_points(player_sprite.points)
    show_player_health(player_sprite.health)
    show_shop_label()

    player_group.update()
    player_group.draw(screen)

    opponents_group.update()
    opponents_group.draw(screen)

    pygame.display.flip()
    fps_clock.tick(fps)
