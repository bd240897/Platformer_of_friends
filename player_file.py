import pygame
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, bloks, coins):
        pygame.sprite.Sprite.__init__(self)
        # отрисуем персонажа
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # поля персонажа
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.onGround = False
        self.rect.centerx = WIDTH / 2 # базовое расположение
        self.rect.bottom = HEIGHT - 50 - 2*PLATFORM_HEIGHT
        self.selected_coins = 0
        # чтоб разбить на несколько классов

        self.bloks = bloks
        self.coins = coins

    def go_lef(self):
        self.speed_x = -8

    def go_right(self):
        self.speed_x = 8

    def go_jump(self):
        if self.onGround:
            self.speed_y = -16

    def go_down(self):
        self.speed_y = +8

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.speed_x = 0

    def check_onGraound(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.bloks, False)
        self.rect.y -= 2

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0:
            self.onGround = True

    def select_coins(self, coins):
        selected_coins = pygame.sprite.spritecollide(self, coins, True)
        for selected_coin in selected_coins:
            self.selected_coins += 1
            print(self.selected_coins)

    def update(self):
        self.onGround = False
        self.check_onGraound()

        if not self.onGround:
            if self.speed_y == 0:
                self.speed_y = 1
            else:
                self.speed_y += 1

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

        self.select_coins(self.coins)
