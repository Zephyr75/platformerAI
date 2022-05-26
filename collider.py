import pygame
from pygame import RLEACCEL, K_UP

from colors import white, black, red
from constants import SCREEN_HEIGHT


class Collider(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Collider, self).__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(red)
        self.rect = self.image.get_rect(
            center=(x, y)
        )
