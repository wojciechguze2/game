import os
import sys

import pygame
from pygame.locals import *

import const
import sprites

pygame.init()

# fonts
monospace_12 = pygame.font.SysFont(*const.monospace_12)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s, %s' % (const.WINDOW_POSITION_X, const.WINDOW_POSITION_Y)

fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(const.WINDOW_SIZE)
pygame.display.set_caption("pygame arrow shooting")

player_sprite = sprites.Player(const.BLACK, 30, 40, const.PLAYER_SPRITE_IMAGE_PATH)
player_sprite.rect.x, player_sprite.rect.y = 30, 500

# arrow_sprite = sprites.Player(const.BLACK, 3, 5, const.ARROW_SPRITE_IMAGE_PATH)
# arrow_sprite.rect.x, arrow_sprite.rect.y = 30, 500

sprites_list = pygame.sprite.Group(player_sprite)  # , arrow_sprite)

clock = pygame.time.Clock()
pygame.display.update()

while True:
    screen.fill(const.WHITE)
    keyPressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if keyPressed[pygame.K_ESCAPE]:
        break

    if keyPressed[pygame.K_LEFT] and player_sprite.rect.left > const.WINDOW_PADDING:
        player_sprite.moveLeft(const.PLAYER_SPEED)

    if keyPressed[pygame.K_RIGHT] and player_sprite.rect.right < const.WINDOW_WIDTH - const.WINDOW_PADDING:
        player_sprite.moveRight(const.PLAYER_SPEED)

    if keyPressed[pygame.K_DOWN] and player_sprite.rect.bottom < const.WINDOW_HEIGHT - const.WINDOW_PADDING:
        player_sprite.moveDown(const.PLAYER_SPEED)

    if keyPressed[pygame.K_UP] and player_sprite.rect.top > const.WINDOW_PADDING:
        player_sprite.moveUp(const.PLAYER_SPEED)

    sprites_list.update()
    sprites_list.draw(screen)
    pygame.display.flip()
    fpsClock.tick(fps)
