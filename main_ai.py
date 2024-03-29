import os
import sys
from math import ceil
import matplotlib.pyplot as plt
import pygame
from pygame.locals import (
    K_SPACE,
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
import neat

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
max_array = []
full_speed = 300

def load_chunk(offset, first):
    rand = random.randint(0, 3)
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
            if next_chunk[i][j] == 1:
                ground_placed = Block(offset + j * 32, 160 + i * 32, "ground.png")
                all_sprites.add(ground_placed)
                blocks.add(ground_placed)
                all_blocks.append(1)
            elif next_chunk[i][j] == 2:
                bottom_placed = Block(offset + j * 32, 160 + i * 32, "bottomGround.png")
                all_sprites.add(bottom_placed)
                blocks.add(bottom_placed)
                all_blocks.append(1)
            elif next_chunk[i][j] == 3:
                platform_placed = Block(offset + j * 32, 160 + i * 32, "platform.png")
                all_sprites.add(platform_placed)
                blocks.add(platform_placed)
                all_blocks.append(1)
            else:
                all_blocks.append(0)


def eval_genomes(genomes, config):
    global ge, networks,players, all_blocks, all_sprites, blocks
    clock = pygame.time.Clock()
    ge = []
    networks = []
    players = []
    distance = 5
    all_blocks = []
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    framerate = full_speed
    max_distance = 0

    # Load map
    load_chunk(64, True)
    for k in range(1000):
        load_chunk(64 + 32 * k * 3, False)

    for genome_id, genome in genomes:
        player = Player()
        players.append(player)
        ge.append(genome)
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0

    running = True
    while running:
        # Quit on Esc or window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                plt.plot(max_array)
                plt.show()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    plt.plot(max_array)
                    plt.show()
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if framerate == full_speed:
                        framerate = 15
                    else:
                        framerate = full_speed

        # Set background
        screen.fill(black)

        # Compute AI inputs
        for i, player in enumerate(players):
            inputs = [distance, player.rect.centery]
            for b in range(15):
                inputs.append(all_blocks[b + ceil(distance)])
            output = networks[i].activate(inputs)
            up = False
            right = False
            if output[0] > .5:
                up = player.bottom_left(blocks) or player.bottom_right(blocks)
            if output[1] > .5:
                right = not player.top_right(blocks) and not player.right(blocks)
            if right:
                player.life = 100
                ge[i].fitness += 1
                distance += 1/32
            else:
                player.life -= 1
            player.update(up, blocks, screen)
            if player.rect.centery >= SCREEN_HEIGHT or player.right(blocks) or player.life <= 0:
                ge[i].fitness -= 1
                ge.pop(i)
                networks.pop(i)
                players.pop(i)
            blocks.update(right)

        # Update visuals
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        for player in players:
            screen.blit(player.image, player.rect)
        pygame.display.flip()

        # Define framerate
        clock.tick(framerate)

        if distance > max_distance:
            max_distance = distance

        if len(players) == 0:
            print(population.generation, "->", max_distance)
            max_array.append(max_distance)
            break


def run(path):
    global population
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        path
    )

    population = neat.Population(config)
    population.run(eval_genomes, 1000)


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')
run(config_path)

plt.plot(max_array)
plt.show()
pygame.quit()
sys.exit()