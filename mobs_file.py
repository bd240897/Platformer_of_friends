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
        self.rect.center = (x - PLATFORM_WIDTH/2, y - PLATFORM_HEIGHT/2)
        # поля персонажа
        self.speed_x = 1
        self.speed_y = 0
        # флаги для проверки что моб стоит на одном блоке
        self.one_blok_below_left = False
        self.one_blok_below_right = False
        # взаимодействует с блоками
        self.bloks = bloks

    @staticmethod
    def random_mob_position():
        """Выбор случайно позиции для моба"""
        i, j = (0, 0)
        while not sum(level_digit[i][j]) > 0:
            i = random.randint(1, num_blok_x - 2)
            j = random.randint(1, num_blok_y - 2)
        return level_digit[i][j]

    def collision_edge(self):
        """Моб проверяет что это край карты и разворачивается"""
        # переменная для проверки что всего один блок под собой
        self.one_blok_below_left, self.one_blok_below_right = False, False

        # проверка края справа и разворот
        if self.speed_x > 0:
            self.rect.y += 10
            self.rect.x += MOB_SIZE
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = -1
                self.one_blok_below_left = True
            self.rect.y -= 10
            self.rect.x -= MOB_SIZE

        # проверка края слева и разворот
        if self.speed_x < 0:
            self.rect.y += 10
            self.rect.x -= MOB_SIZE
            hits = pygame.sprite.spritecollide(self, self.bloks, False)
            if len(hits) == 0:
                self.speed_x = 1
                self.one_blok_below_right = True
            self.rect.y -= 10
            self.rect.x += MOB_SIZE

        # если стоим на одном блкое то не двигаемся
        if self.one_blok_below_left and self.one_blok_below_right:
            self.speed_x = 0

    def update(self, *args, **kwargs):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.collision_edge()