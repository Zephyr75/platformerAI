import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, RLEACCEL

from collider import Collider
from colors import white
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    jump = 0

    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("hero.png").convert()
        self.image.set_colorkey(white, RLEACCEL)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(
            center=(128, 64)
        )

    def top_right(self, blocks):
        col = Collider(self.rect.centerx + 8, self.rect.centery - 12)
        return pygame.sprite.spritecollideany(col, blocks)

    def top_left(self, blocks):
        col = Collider(self.rect.centerx - 8, self.rect.centery - 12)
        return pygame.sprite.spritecollideany(col, blocks)

    def bottom_right(self, blocks):
        col = Collider(self.rect.centerx + 8, self.rect.centery + 16)
        return pygame.sprite.spritecollideany(col, blocks)

    def bottom_left(self, blocks):
        col = Collider(self.rect.centerx - 8, self.rect.centery + 16)
        return pygame.sprite.spritecollideany(col, blocks)

    def right(self, blocks):
        col = Collider(self.rect.centerx + 16, self.rect.centery)
        return pygame.sprite.spritecollideany(col, blocks)

    def left(self, blocks):
        col = Collider(self.rect.centerx - 16, self.rect.centery)
        return pygame.sprite.spritecollideany(col, blocks)

    def update(self, pressed_keys, blocks, screen):
        col = Collider(self.rect.centerx - 16, self.rect.centery)
        screen.blit(col.image, col.rect)

        top_right = self.top_right(blocks)
        bottom_right = self.bottom_right(blocks)
        top_left = self.top_left(blocks)
        bottom_left = self.bottom_left(blocks)

        if not bottom_left and not bottom_right and self.jump <= 0:
            self.rect.move_ip(0, 5)
        if not top_right and not top_left and self.jump > 0:
            self.jump -= 5
            self.rect.move_ip(0, - self.jump / 10)
        if top_right or top_left:
            self.jump = 0
        if pressed_keys[K_UP] and (bottom_left or bottom_right):
            self.jump = 100
        if self.rect.centery >= SCREEN_HEIGHT:
            exit(0)

