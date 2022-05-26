import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from collider import Collider
from colors import black, grey
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random

from enemy import Enemy
from map import ground, hole, platform, stairs
from platform import Platform
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

player = Player()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 5000)

enemies = pygame.sprite.Group()
platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()


def load_chunk(offset):
    rand = random.randint(0, 4)
    next_chunk = []
    if rand == 0:
        next_chunk = ground
    elif rand == 1:
        next_chunk = hole
    elif rand == 2:
        next_chunk = stairs
    else:
        next_chunk = platform
    for i in range(10):
        for j in range(5):
            print(i, j)
            if next_chunk[i][j] == 1:
                ground_placed = Platform(offset + j * 32, i * 32, "ground.png")
                all_sprites.add(ground_placed)
                platforms.add(ground_placed)
            elif next_chunk[i][j] == 2:
                bottom_placed = Platform(offset + j * 32, i * 32, "bottomGround.png")
                all_sprites.add(bottom_placed)
                platforms.add(bottom_placed)
            elif next_chunk[i][j] == 3:
                platform_placed = Platform(offset + j * 32, i * 32, "platform.png")
                all_sprites.add(platform_placed)
                platforms.add(platform_placed)


load_chunk(32)
load_chunk(32+32*5)
load_chunk(32+32*10)
load_chunk(32+32*15)
load_chunk(32+32*20)
load_chunk(32+32*25)

top_right_collision = False
bottom_right_collision = False
top_left_collision = False
bottom_left_collision = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        """elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)"""

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, platforms, screen)
    enemies.update()
    platforms.update(pressed_keys, player, platforms)

    screen.fill(black)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
