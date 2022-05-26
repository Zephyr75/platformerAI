import random
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL

from colors import white
from constants import SCREEN_WIDTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Platform, self).__init__()
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(white, RLEACCEL)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self, pressed_keys, player, blocks):
        if pressed_keys[K_LEFT] and not player.top_left(blocks) and not player.left(blocks):
            self.rect.move_ip(3, 0)
        if pressed_keys[K_RIGHT] and not player.top_right(blocks) and not player.right(blocks):
            self.rect.move_ip(-3, 0)
