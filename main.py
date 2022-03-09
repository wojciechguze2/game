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

fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode(const.WINDOW_SIZE)
pygame.display.set_caption('pygame player vs opponents shooting game')

player_sprite = sprites.Player(
    image_path=const.PLAYER_SPRITE_IMAGE_PATH,
    x=const.INIT_PLAYER_X,
    y=const.INIT_PLAYER_Y
)

shop_icon = sprites.ShopIcon(
    x=const.WINDOW_WIDTH - const.WINDOW_PADDING - (const.WINDOW_WIDTH * 0.045),
    y=const.WINDOW_HEIGHT * 0.075
)

arrows = []
facing = 1

player_group = pygame.sprite.Group(player_sprite)
opponents_group = pygame.sprite.Group()
icons_group = pygame.sprite.Group(shop_icon)

pygame.display.update()

main_loop_counter = 0
shop_displayed = False  # stops the game


def update_pygame_display(fps=75):
    pygame.display.flip()
    fps_clock.tick(fps)


def show_points(points: int):
    points_label = monospace_12.render('Points: %d' % points, True, const.ORANGE)

    screen.blit(
        points_label,
        (
            const.WINDOW_WIDTH - const.WINDOW_PADDING - (const.WINDOW_WIDTH * 0.05),  # x
            const.WINDOW_HEIGHT * 0.025  # y
        )
    )


def show_player_health(health: int):
    health_label = monospace_12.render('Health: %d' % health, True, const.DARK_GREEN)

    screen.blit(
        health_label,
        (
            const.WINDOW_WIDTH - const.WINDOW_PADDING - (const.WINDOW_WIDTH * 0.055),  # x
            const.WINDOW_HEIGHT * 0.05  # y
        )
    )


shop_item_positions = {}
item_number = 0

for row_number in range(10):  # row
    for col_number in range(10):
        shop_item_positions[item_number] = {
            'x': col_number * 30 + col_number * 30 + const.SHOP_ITEMS_LIST_PADDING_X,
            'y': row_number * 60 + row_number * 60 + const.SHOP_ITEMS_LIST_PADDING_Y
        }
        item_number += 1


def show_shop_menu():
    shop_container = sprites.ShopContainer(screen, color=const.DARK_GREEN)
    shop_group = pygame.sprite.Group(shop_container)

    shop_items = [
        sprites.ShopItem(image_path=const.SHOP_ICON_IMAGE_PATH, item_pos=shop_item_positions[shop_item_number])
        # TODO: change images
        for shop_item_number in range(40)
    ]
    shop_items_group = pygame.sprite.Group(shop_items)

    shop_items_group.update()
    shop_items_group.draw(screen)

    icons_group.update()
    icons_group.draw(screen)

    shop_group.update()
    shop_group.draw(screen)

    update_pygame_display()


def update_sprite_groups():
    player_group.update()
    player_group.draw(screen)

    opponents_group.update()
    opponents_group.draw(screen)

    icons_group.update()
    icons_group.draw(screen)


while True:
    main_loop_counter += 1

    key_pressed = pygame.key.get_pressed()
    player_rect = player_group.sprites()[0].rect

    screen.fill(const.WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            shop_displayed = shop_icon.rect.collidepoint(mouse_pos)

    if key_pressed[pygame.K_ESCAPE]:
        break

    if shop_displayed:
        show_shop_menu()

        continue

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

    if key_pressed[pygame.K_SPACE] and player_sprite.rect.left:
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
            resistance=randint(1, 5),
            speed=2 + main_loop_counter / 10000
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
        opponent.move_towards_player(player_rect)
        opponent.attack_player(player_sprite, main_loop_counter)

    show_points(player_sprite.points)
    show_player_health(player_sprite.health)
    update_sprite_groups()
    update_pygame_display()
