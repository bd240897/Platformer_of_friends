import numpy as np
import pygame
from constants import *

class Sword(pygame.sprite.Sprite):
    """ Класс для меча у персонажа"""

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((40, 5), pygame.SRCALPHA)
        # self.image.fill(RED)
        # self.orig_image = self.image
        player_img = pygame.image.load(os.path.join(img_dir, "sword_1.png")).convert()
        player_img = pygame.transform.scale(player_img, (40, 20))
        player_img.set_colorkey(WHITE)
        self.image = player_img
        self.orig_image = player_img.copy()
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.bottomright = self.player.rect.topleft

        # атрибуты
        self.up_flag = True
        self.sword_side = None
        self.DATA = {}

    def up_sword(self, sword_side):
        """Поднять мечь"""
        self.sword_side = sword_side
        if self.sword_side == 'left':
            self.image = pygame.transform.rotate(self.orig_image, -45)
            self.rect = self.image.get_rect()
            self.rect.bottomright = self.add_to_tuple(self.player.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y)
        elif self.sword_side == 'right':
            self.image = pygame.transform.rotate(self.orig_image, -135)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.add_to_tuple(self.player.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y)
        self.up_flag = True
        self.down_time = 0

    def down_sword(self):
        """Поднять мечь"""
        if self.sword_side == 'left':
            self.image = pygame.transform.rotate(self.orig_image, +45)
            self.rect = self.image.get_rect()
            self.rect.topright = self.add_to_tuple(self.player.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y - PLAYER_HEIGHT/2)
        elif self.sword_side == 'right':
            self.image = pygame.transform.rotate(self.orig_image, +135)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.add_to_tuple(self.player.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y - PLAYER_HEIGHT/2)
        self.up_flag = False
        self.down_time = 0
        self.down_time = pygame.time.get_ticks()

    def update_sword_coord(self):
        """Обновление положения меча на экране"""
        if self.player.sword_exist and self.sword_side == 'left':
            if self.up_flag:
                self.rect.bottomright = self.add_to_tuple(self.player.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y)
            else:
                self.rect.topright = self.add_to_tuple(self.player.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y - PLAYER_HEIGHT/2)
        elif self.player.sword_exist and self.sword_side == 'right':
            if self.up_flag:
                self.rect.bottomleft = self.add_to_tuple(self.player.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y)
            else:
                self.rect.topleft = self.add_to_tuple(self.player.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y - PLAYER_HEIGHT/2)

    def update(self):
        if self.up_flag:
            pass
        elif not self.up_flag:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.down_time > FPS * 3:
                self.up_sword(self.sword_side)

        self.update_sword_coord()

    @staticmethod
    def add_to_tuple(mass, x_add, y_add):
        mass_result = (mass[0] + x_add, mass[1] + y_add)
        return mass_result