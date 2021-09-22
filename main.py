# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from player_file import Player
from coin_file import Coins
from mobs_file import Mob
from platform_file import Platform
from sword_file import Sword
from constants import *
from menu import Menu
from menu import Menu
from camera_file import Camera

class Main():
    def __init__(self):
        # Создаем игру и окно
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.create_objects()

        # поля класса
        self.main_music_flag = 'init'
        self.WAS_START_SCREEN = False
        self.running = True
        self.camera = Camera(Camera.camera_configure, TOTAL_LEVEL_WEIGHT, TOTAL_LEVEL_HEIGHT)

########################################################################################################################
    """Креаторы объектов"""

    def crete_group(self):
        """Создаем группы для хранения объектов"""
        self.all_bloks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_coins = pygame.sprite.Group()
        self.all_mobs = pygame.sprite.Group()

    def create_player(self):
        """Создим персанажа"""
        self.player = Player(TOTAL_LEVEL_WEIGHT//2, PLATFORM_HEIGHT*3, self.all_bloks, self.all_coins, self.all_mobs)
        self.all_sprites.add(self.player)

    def create_mobs(self):
        """Создим мобов"""
        for num_mob in range(1, COUNT_MOBS+1):
            mob = Mob(*Mob.random_mob_position(), self.all_bloks)
            self.all_mobs.add(mob)
            self.all_sprites.add(mob)

    def create_sword(self):
        """Создим мечь"""
        sword = Sword(self.player)
        self.player.create_sword(sword)
        self.all_sprites.add(sword)

    def create_platforms(self):
        """Создим уровень и монетки на нем"""
        # рисование уровня
        x = y = 0  # координаты
        for row in level_2:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    one_platform = Platform(x,y)
                    self.all_bloks.add(one_platform)
                    self.all_sprites.add(one_platform)
                if col == "*":
                    one_coin = Coins(x, y)
                    self.all_coins.add(one_coin)
                    self.all_sprites.add(one_coin)
                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

    def create_objects(self):
        """Создим все что создается"""
        self.crete_group()
        self.create_player()
        self.create_platforms()
        self.create_mobs()
########################################################################################################################
        """Работа с музыкой"""

    def play_main_music(self, emurgance_stop=False):
        """Фоновая музыка"""
        pygame.mixer.init()
        if self.main_music_flag == 'init':
            sounds_main_theme = os.path.join(snd_dir, 'main_theme_sounds.mp3')
            pygame.mixer.music.load(sounds_main_theme)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            self.main_music_flag = 'play'
        elif self.main_music_flag == 'stop' or emurgance_stop:
            pygame.mixer.music.pause()

########################################################################################################################
        """Обрабочики событий"""

    def handle_events(self):
        """Обработка кнопок при управлении персом"""
        # запуск стартового экрана
        self.m = Menu(self.screen)
        if not self.WAS_START_SCREEN:
            self.m.run_begin_screen()
            self.WAS_START_SCREEN = True

        # запуск музыки
        self.play_main_music()

        # ивенты НАЖАТИЙ
        for event in pygame.event.get():
            # выход из программы
            if event.type == pygame.QUIT:
                self.running = False
            # запуск меню
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.m.run_menu_outside()
            # ивенты движения (остановка на всякий случай)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.speed_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.speed_x > 0:
                    self.player.stop()
            # ивенты удара и доставания меча
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sword_side = 'left'
                if self.player.sword_exist:
                    self.player.remove_sword()
                else:
                    self.create_sword()
                    self.player.take_sword(sword_side)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                sword_side = 'right'
                if self.player.sword_exist:
                    self.player.remove_sword()
                else:
                    self.create_sword()
                    self.player.take_sword(sword_side)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.make_sword()
        # ивенты движения
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.player.go_lef()
        if keystate[pygame.K_RIGHT]:
            self.player.go_right()
        if keystate[pygame.K_UP]:
            self.player.go_jump()
        if keystate[pygame.K_DOWN]:
            self.player.go_down()

    def handle_end_game(self):
        """Создание окна окончания игры """
        if self.player.win_game:
            self.play_main_music(emurgance_stop=True)
            self.m.run_end_game('win_game')
        if self.player.lose_game:
            self.play_main_music(emurgance_stop=True)
            self.m.run_end_game('lose_game')

    def run(self):
        # Цикл игры
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(FPS)

            # Ввод процесса (события)
            self.handle_events()

            # ОБНОВЛЕНИЕ
            self.screen.fill(BLACK)
            background = BACKGROUND.convert()
            background = pygame.transform.scale(background, (WIDTH_WINDOW, HEIGHT_WINDOW))
            background_rect = background.get_rect()
            self.screen.blit(background, background_rect)

            # работы с камерой
            self.camera.update(self.player)  # центризируем камеру относительно персонажа
            for sprites in self.all_sprites:
                self.screen.blit(sprites.image, self.camera.apply(sprites))
                sprites.update()

            # отрисуем здоровье
            self.player.draw_healf(self.screen)

            # РЕНДЕРИНГ
            pygame.display.flip()
            self.handle_end_game()

class Level():
    def __init__(self):
        self.list_level = [level, level_2]
        self.point_spawn_player = [point_spawn_player_1, point_spawn_player_2]

main = Main()
main.run()