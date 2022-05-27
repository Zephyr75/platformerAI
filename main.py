import pygame
from pygame.locals import (
    K_UP,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
)
from block import Block
from colors import black
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import random
from map import ground, hole, stairs_up, stairs_down, block_up, floating
from player import Player


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Defines if game is controlled by the player or the AI
manual = True

players = pygame.sprite.Group()
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Add single player when controlling the game manually
if manual:
    player = Player()
    players.add(player)
    all_sprites.add(player)


def load_chunk(offset, first):
    rand = random.randint(0, 7)
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
    else:
        next_chunk = block_up
    for i in range(5):
        for j in range(3):
            print(i, j)
            if next_chunk[i][j] == 1:
                ground_placed = Block(offset + j * 32, 160 + i * 32, "ground.png")
                all_sprites.add(ground_placed)
                blocks.add(ground_placed)
            elif next_chunk[i][j] == 2:
                bottom_placed = Block(offset + j * 32, 160 + i * 32, "bottomGround.png")
                all_sprites.add(bottom_placed)
                blocks.add(bottom_placed)
            elif next_chunk[i][j] == 3:
                platform_placed = Block(offset + j * 32, 160 + i * 32, "platform.png")
                all_sprites.add(platform_placed)
                blocks.add(platform_placed)


# Load map
load_chunk(32, True)
for k in range(100):
    load_chunk(32 + 32 * k * 3, False)

while running:
    # Quit on Esc or window closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # Get inputs
    if manual:
        pressed_keys = pygame.key.get_pressed()
        right = pressed_keys[K_RIGHT] and not player.top_right(blocks) and not player.right(blocks)
        up = pressed_keys[K_UP] and (player.bottom_left(blocks) or player.bottom_right(blocks))
    else:
        right = False
        up = False

    player.update(up, blocks, screen)
    blocks.update(right)

    # Update visuals
    screen.fill(black)
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    pygame.display.flip()

    # Define framerate
    clock.tick(30)

pygame.quit()
