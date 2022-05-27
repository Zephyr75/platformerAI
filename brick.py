import random
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL

from colors import white
from constants import SCREEN_WIDTH


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Brick, self).__init__()
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(white, RLEACCEL)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self, left, right):
        if left:
            self.rect.move_ip(5, 0)
        if right:
            self.rect.move_ip(-5, 0)
