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

from brick import Brick
from collider import Collider
from colors import black, grey
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random

from enemy import Enemy
from map import ground, hole, stairs_up, stairs_down, trap_up, trap_down, floating
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


def load_chunk(offset, first):
    rand = random.randint(0, 7)
    next_chunk = []
    if first:
        next_chunk = ground
    elif rand == 0:
        next_chunk = ground
    elif rand == 1:
        next_chunk = hole
    elif rand == 2:
        next_chunk = stairs_up
    elif rand == 3:
        next_chunk = stairs_down
    elif rand == 4:
        next_chunk = floating
    elif rand == 5:
        next_chunk = trap_up
    else:
        next_chunk = trap_down

    for i in range(5):
        for j in range(3):
            print(i, j)
            if next_chunk[i][j] == 1:
                ground_placed = Brick(offset + j * 32, 160 + i * 32, "ground.png")
                all_sprites.add(ground_placed)
                platforms.add(ground_placed)
            elif next_chunk[i][j] == 2:
                bottom_placed = Brick(offset + j * 32, 160 + i * 32, "bottomGround.png")
                all_sprites.add(bottom_placed)
                platforms.add(bottom_placed)
            elif next_chunk[i][j] == 3:
                platform_placed = Brick(offset + j * 32, 160 + i * 32, "platform.png")
                all_sprites.add(platform_placed)
                platforms.add(platform_placed)


load_chunk(32, True)

for i in range(100):
    load_chunk(32 + 32 * i * 3, False)

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

    left = pressed_keys[K_LEFT] and not player.top_left(platforms) and not player.left(platforms)
    right = pressed_keys[K_RIGHT] and not player.top_right(platforms) and not player.right(platforms)
    platforms.update(left, right)

    screen.fill(black)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
