import pygame
from constants import *
import time

class Player(pygame.sprite.Sprite):
    """ Класс для описания игрока и его действий """
    def __init__(self, bloks, coins, mobs):
        pygame.sprite.Sprite.__init__(self)
        # отрисуем персонажа
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
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
        self.sword_exist = False

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

    def take_sword(self, sword):
        """Взять мечь"""
        self.sword = sword
        self.sword_exist = True

    def remove_sword(self):
        self.sword.kill()
        self.sword_exist = False

    def update_sword_coord(self):
        """Обновление положения меча на экране"""
        if self.sword_exist:
            if self.sword.up_flag:
                self.sword.rect.bottomright = self.rect.topleft
            else:
                self.sword.rect.topright = self.rect.topleft

    def update(self):
        self.gravitation()
        self.collision_coins()
        self.collision_player_and_mobs()
        # есть мечь опщен проверять колизию
        if not self.sword.up_flag: self.collision_sword_mobs()

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

    def make_sword(self):
        self.down_sword()

    def update(self):
        if self.up_flag:
            pass
        elif not self.up_flag:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.down_time > FPS*3:
                self.up_sword()
                