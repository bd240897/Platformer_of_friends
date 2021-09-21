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
        player_img = pygame.transform.scale(player_img, (PLAYER_HEIGHT, PLAYER_WIDTH))
        player_img.set_colorkey(GRAY)
        self.image = player_img
        self.rect = self.image.get_rect()

        # поля персонажа
        self.speed_x = 0
        self.speed_y = 0
        self.onGround = False # флаг - стоит ли персонаж не земле

        # точка спавна перса
        self.rect.centerx = WIDTH_WINDOW / 2 # базовое расположение
        self.rect.bottom = HEIGHT_WINDOW - 50 - 2*PLATFORM_HEIGHT
        self.orig_coord = self.rect.center

        # взаиодействие с другими объектами
        self.bloks = bloks
        self.coins = coins
        self.mobs = mobs

        # очки персонажа
        self.sword_exist = None
        self.healf = 100
        self.selected_coins = 0 # cчетчик собраных монет
        self.time_player_and_mobs = 0

        # игра
        self.count_kill_mobs = 0
        self.win_game = False
        self.lose_game = False
        self.sounds_play = False

        # создадим музыку
        self.create_music()

    def create_music(self):
        "Cоздает обхекты для музыки"
        pygame.mixer.init()
        self.sounds_make_sword = pygame.mixer.Sound(os.path.join(snd_dir, 'make_sword_2.wav'))
        self.sounds_kill_mob = pygame.mixer.Sound(os.path.join(snd_dir, 'kill_mobs_2.wav'))
        self.sounds_take_coin = pygame.mixer.Sound(os.path.join(snd_dir, 'take_coins_2.wav'))
        self.sounds_take_damage = pygame.mixer.Sound(os.path.join(snd_dir, 'take_damage_2.wav'))
        # настройка музыки
        self.sounds_take_coin.set_volume(0.5)
        self.sounds_make_sword.set_volume(0.5)
        self.sounds_kill_mob.set_volume(0.5)

    def hanler_sounds(self, sounds):
        if not self.sounds_play:
            self.sounds_play = True
            sounds.play()
            self.sounds_play = False

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
            # self.sounds_take_coin.play()
            self.hanler_sounds(self.sounds_take_coin)

    def collision_sword_and_mobs(self):
        """Взаиодействие меча с врагами с врагами"""
        hits = pygame.sprite.spritecollide(self.sword, self.mobs, False)
        for hit in hits:
            hit.kill()
            self.count_kill_mobs += 1
            self.selected_coins += 2
            # self.sounds_kill_mob.play()
            self.hanler_sounds(self.sounds_kill_mob)

        if COUNT_MOBS == self.count_kill_mobs:
            self.win_game = True


    def collision_player_and_mobs(self):
        """Взаиодействие с врагами"""
        hits = pygame.sprite.spritecollide(self, self.mobs, False)
        curr_time = pygame.time.get_ticks()
        if self.time_player_and_mobs == 0:
            for hit in hits:
                self.time_player_and_mobs = pygame.time.get_ticks()
                self.healf -= 30
                # self.sounds_take_damage.play()
                self.hanler_sounds(self.sounds_take_damage)
        elif curr_time - self.time_player_and_mobs > 1000:
            for hit in hits:
                self.time_player_and_mobs = pygame.time.get_ticks()
                self.healf -= 30
                # self.sounds_take_damage.play()
                self.hanler_sounds(self.sounds_take_damage)
        if self.healf == 0 or self.healf < 0:
            self.lose_game = True

    def draw_healf(self, screen):
        # шрифт
        font_name = pygame.font.match_font('arial')
        size = PLATFORM_HEIGHT
        font = pygame.font.Font(font_name, size)
        # здоровье
        text_healf = 'healf: ' + str(self.healf)
        image_healf = font.render(text_healf, True, WHITE)
        # очки
        text_points = 'point: ' + str(self.selected_coins)
        image_pints = font.render(text_points, True, WHITE)
        # прямоугольник
        image_rect = pygame.Surface((PLATFORM_WIDTH*4+PLATFORM_HEIGHT*0.1, PLATFORM_HEIGHT*2+PLATFORM_HEIGHT*0.2))
        image_rect.fill(BLACK)
        screen.blit(image_rect, (0,0))
        # рендер текста
        screen.blit(image_healf, (PLATFORM_WIDTH/3,0))
        screen.blit(image_pints, (PLATFORM_WIDTH/3, PLATFORM_HEIGHT))

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

    def remove_sword(self):
        self.sword.kill()
        self.sword_exist = False

    def make_sword(self):
        if self.sword_exist:
            self.sword.down_sword()
            # self.sounds_make_sword.play()
            self.hanler_sounds(self.sounds_make_sword)

    def update(self):
        self.gravitation()
        self.collision_coins()
        self.collision_player_and_mobs()
        # есть мечь взять и опщен проверять колизию
        if self.sword_exist and not self.sword.up_flag: self.collision_sword_and_mobs()

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