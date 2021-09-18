import pygame
from constants import *
import time
from sword_file import Sword
import os

class Player(pygame.sprite.Sprite):
    """ Класс для описания игрока и его действий """
    def __init__(self, bloks, coins, mobs):
        pygame.sprite.Sprite.__init__(self)
        # # отрисуем персонажа
        # self.image = pygame.Surface((30, 40))
        # self.image.fill(RED)
        player_img = pygame.image.load(os.path.join(img_dir, "player_1.png")).convert()
        player_img = pygame.transform.scale(player_img, (PLATFORM_WIDTH, int(PLATFORM_HEIGHT*1.5)))
        player_img.set_colorkey(GRAY)
        self.image = player_img

        self.rect = self.image.get_rect()

        # поля персонажа
        self.speed_x = 0
        self.speed_y = 0
        self.onGround = False # флаг - стоит ли персонаж не земле

        # точка спавна перса
        self.rect.centerx = WIDTH / 2 # базовое расположение
        self.rect.bottom = HEIGHT - 50 - 2*PLATFORM_HEIGHT

        # cчетчик собраных монет
        self.selected_coins = 0

        # взаиодействие с другими объектами
        self.bloks = bloks
        self.coins = coins
        self.mobs = mobs
        self.sword_exist = None

    def go_lef(self):
        """Шаг влево"""
        self.speed_x = -8

    def go_right(self):
        """Шаг вправо"""
        self.speed_x = 8

    def go_jump(self):
        """Прыжок, если перс стоит не земле """
        if self.onGround:
            self.speed_y = -16
            
    def go_down(self):
        """Еще не реулизовано - присесть"""
        pass

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.speed_x = 0

    def collision_onGraund(self):
        """Проверка на земле ли мы - сдвиг вниз, проверка колизии, сдвиг вверз"""
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.bloks, False)
        self.rect.y -= 2

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0:
            self.onGround = True

    def collision_coins(self):
        """Подбор коинов"""
        selected_coins = pygame.sprite.spritecollide(self, self.coins, True)
        for selected_coin in selected_coins:
            self.selected_coins += 1
            print(self.selected_coins)

    def collision_sword_mobs(self):
        """Взаиодействие меча с врагами с врагами"""
        hits = pygame.sprite.spritecollide(self.sword, self.mobs, False)
        for hit in hits:
            hit.kill()

    def collision_player_and_mobs(self):
        """Взаиодействие с врагами"""
        pass

    def gravitation(self):
        """Работа гравитации"""
        self.onGround = False
        self.collision_onGraund()

        if not self.onGround:
            if self.speed_y == 0:
                self.speed_y = 1
            else:
                self.speed_y += 1

    def collision_bloks(self):
        """НАверно стоит переместить метод сюда пока он ниже"""
        pass

    def create_sword(self, sword):
        self.sword = sword

    def take_sword(self, sword_side):
        """Взять мечь"""
        self.sword.up_sword(sword_side)
        self.sword_exist = True
        self.sword_side = sword_side

    def remove_sword(self):
        self.sword.kill()
        self.sword_exist = False

    def make_sword(self):
        if self.sword_exist:
            self.sword.down_sword(self.sword_side)

    def update_sword_coord(self):
        """Обновление положения меча на экране"""
        if self.sword_exist and self.sword_side == 'left':
            if self.sword.up_flag:
                self.sword.rect.bottomright = self.sword.add_to_tuple(self.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y)
            else:
                self.sword.rect.topright = self.sword.add_to_tuple(self.rect.topleft, SWORD_SHIFT_X, SWORD_SHIFT_Y)
        elif self.sword_exist and self.sword_side == 'right':
            if self.sword.up_flag:
                self.sword.rect.bottomleft = self.sword.add_to_tuple(self.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y)
            else:
                self.sword.rect.topleft = self.sword.add_to_tuple(self.rect.topright, -SWORD_SHIFT_X, SWORD_SHIFT_Y)

    def update(self):
        self.gravitation()
        self.collision_coins()
        self.collision_player_and_mobs()
        # есть мечь взять и опщен проверять колизию
        if self.sword_exist and not self.sword.up_flag: self.collision_sword_mobs()

        self.rect.x += self.speed_x
        hits = pygame.sprite.spritecollide(self, self.bloks, False)
        for hit in hits:
            if self.speed_x > 0:
                self.rect.right = hit.rect.left
            elif self.speed_x < 0:
                self.rect.left = hit.rect.right
            self.speed_x = 0

        self.rect.y += self.speed_y
        hits = pygame.sprite.spritecollide(self, self.bloks, False)
        for hit in hits:
            if self.speed_y > 0:
                self.rect.bottom = hit.rect.top
            elif self.speed_y < 0:
                self.rect.top = hit.rect.bottom
            self.speed_y = 0

        self.update_sword_coord()