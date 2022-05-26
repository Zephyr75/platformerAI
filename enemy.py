import random
import pygame
from pygame import RLEACCEL

from colors import white
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("enemy.png").convert()
        self.image.set_colorkey(white, RLEACCEL)
        self.image = pygame.transform.scale(self.image, (16, 32))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
