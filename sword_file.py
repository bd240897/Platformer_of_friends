import pygame
from constants import *

class Sword(pygame.sprite.Sprite):
    """ Класс для меча у персонажа"""

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 5), pygame.SRCALPHA)
        self.image.fill(RED)
        self.orig_image = self.image
        self.image = pygame.transform.rotate(self.image, -45)
        self.rect = self.image.get_rect()

        # мечь спавнится в правом угла перса
        self.player = player
        self.rect.bottomright = self.player.rect.topleft

        # атрибуты
        self.up_flag = True

    def up_sword(self):
        """Поднять мечь"""
        self.image = pygame.transform.rotate(self.orig_image, -45)
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.player.rect.topleft
        self.up_flag = True
        self.down_time = 0

    def down_sword(self):
        self.down_time = pygame.time.get_ticks()
        """Опустить мечь"""
        self.image = pygame.transform.rotate(self.orig_image, +45)
        self.rect = self.image.get_rect()
        self.rect.topright = self.player.rect.topleft
        self.up_flag = False
        self.down_time = pygame.time.get_ticks()

    def update(self):
        if self.up_flag:
            pass
        elif not self.up_flag:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.down_time > FPS * 3:
                self.up_sword()
