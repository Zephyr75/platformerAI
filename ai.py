import os

import neat

from player import Player


def eval_genomes(genomes, config):
    ge = []
    nets = []
    players = []

    for genome_id, genome in genomes:
        players.append(Player())
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    for i, player in enumerate(players):
        output = nets[i].activate(
                                   #all inputs
                                            )
        if output[0] > .5 and not jumping:
            jump


collision
        ge[i].fitness -= 1
        ge.pop(index)
        nets.pop(index)

