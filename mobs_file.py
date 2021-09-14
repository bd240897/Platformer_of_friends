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
        self.one_blok_below_left = False
        self.one_blok_below_right = False

        self.bloks = bloks

    def update(self, *args, **kwargs):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.cheсk_edge()

    def cheсk_edge(self):
        # переменная для проверки что всего один блок под собой
        self.one_blok_below_left, self.one_blok_below_right = False, False

        if self.speed_x > 0:
            self.rect.y += 10
            self.rect.x += MOB_SIZE
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = -1
                self.one_blok_below_left = True
            self.rect.y -= 10
            self.rect.x -= MOB_SIZE

        if self.speed_x < 0:
            self.rect.y += 10
            self.rect.x -= MOB_SIZE
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = 1
                self.one_blok_below_right = True
            self.rect.y -= 10
            self.rect.x += MOB_SIZE

        if self.one_blok_below_left and self.one_blok_below_right:
            self.speed_x = 0

