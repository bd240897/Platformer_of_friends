import pygame
from constants import *


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # поля персонажа
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.rect.center = (x, y)
    def update(self):
        pass
