import pygame
from constants import *


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SIZE_OF_COIN, SIZE_OF_COIN))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # поля персонажа
        self.speed_x = 0
        self.speed_y = 0
        self.length_way = 0 # путь колебания коина

    def coins_up(self):
        """Колебание коина вверх-вниз"""
        self.rect.y += self.speed_y
        self.length_way += self.speed_y

        if self.length_way == 0:
            self.speed_y = +1
        if self.length_way == PLATFORM_HEIGHT - SIZE_OF_COIN/2:
            self.speed_y = -1

    def update(self):
        self.coins_up()

