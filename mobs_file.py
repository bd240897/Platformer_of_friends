import pygame
from constants import *
# from main import *
import random

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, bloks):
        pygame.sprite.Sprite.__init__(self)
        # отрисуем персонажа
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x - PLATFORM_WIDTH/2,y - PLATFORM_HEIGHT/2)

        # поля персонажа
        self.x_start = x
        self.y_start = y
        self.speed_x = 1
        self.speed_y = 0

        self.bloks = bloks

    def update(self, *args, **kwargs):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.cheсk_edge()

    def cheсk_edge(self):
        if self.speed_x > 0:
            self.rect.y += 10
            self.rect.x += PLATFORM_HEIGHT
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = -1
            self.rect.y -= 10
            self.rect.x -= PLATFORM_HEIGHT
        if self.speed_x < 0:
            self.rect.y += 10
            self.rect.x -= PLATFORM_HEIGHT
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = 1
            self.rect.y -= 10
            self.rect.x += PLATFORM_HEIGHT

        # i = 11
        # j = 7
        # while sum(level_digit[i][j]):
        #     j += 1
        #     print('asda')
        #
        # if level_digit[i][9][0] < self.rect.x:
        #     self.speed_x = 0


