import pygame
from constants import *
import random

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, bloks):
        pygame.sprite.Sprite.__init__(self)
        # отрисуем персонажа
        # self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(GREEN)
        mob_img = pygame.image.load(os.path.join(img_dir, "germ_pearson_2.png")).convert()
        mob_img = pygame.transform.scale(mob_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT*2))
        mob_img.set_colorkey(PURPUR)
        self.image = mob_img

        self.rect = self.image.get_rect()
        self.rect.center = (x - PLATFORM_WIDTH/2, y - PLATFORM_HEIGHT*2/2)
        # поля персонажа
        self.speed_x = 1
        self.speed_y = 0
        # флаги для проверки что моб стоит на одном блоке
        self.one_blok_below_left = False
        self.one_blok_below_right = False
        # взаимодействует с блоками
        self.bloks = bloks

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