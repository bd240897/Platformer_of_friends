import pygame
from constants import *


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

    def collision_mobs(self):
        """Взаиодействие с врагами"""
        hits = pygame.sprite.spritecollide(self, self.mobs, False)
        for hit in hits:
            hit.kill()

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

    def keep_sword(self, sword):
        """Взять мечь"""
        self.sword = sword
        self.sw_image = self.sword.image
        self.sword.image = pygame.transform.rotate(self.sword.image, -45)
        self.sword.rect = self.sword.image.get_rect()
        self.sword.rect.bottomright = self.rect.topleft
        self.sword_flag_up = True

    def up_sword(self):
        """Поднять мечь"""
        self.sword.image = pygame.transform.rotate(self.sword.orig_image, -45)
        self.sword.rect = self.sword.image.get_rect()
        self.sword.rect.bottomright = self.rect.topleft
        self.sword_flag_up = True

    def down_sword(self):
        """Опустить мечь"""
        self.sword.image = pygame.transform.rotate(self.sword.orig_image, +45)
        self.sword.rect = self.sword.image.get_rect()
        self.sword.rect.topright = self.rect.topleft
        self.sword_flag_up = False

    def update_sword_coord(self):
        """Обновление положения меча на экране"""
        if self.sword_flag_up:
            self.sword.rect.bottomright = self.rect.topleft
        else:
            self.sword.rect.topright = self.rect.topleft

    def update(self):
        self.gravitation()
        self.collision_coins()
        self.collision_mobs()

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 5), pygame.SRCALPHA)
        self.image.fill(RED)
        self.orig_image = self.image
        self.rect = self.image.get_rect()

    def update(self):
        pass