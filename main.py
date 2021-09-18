# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from player_file import *
from constants import *
from coin_file import *
from mobs_file import *
from platform_file import Platform
import random

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# cоздаим группы и добави туда объекты
all_bloks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_coins = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()

def create_player():
    global player
    player = Player(all_bloks, all_coins, all_mobs)
    all_sprites.add(player)

def create_mobs():
    for num_mob in range(1,4):
        mob = Mob(*Mob.random_mob_position(), all_bloks)
        all_mobs.add(mob)
        all_sprites.add(mob)

def create_sword(player):
    sword = Sword(player)
    player.take_sword(sword)
    all_sprites.add(sword)

def create_platforms():
    # рисование уровня
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                one_platform = Platform(x, y)
                all_bloks.add(one_platform)
                all_sprites.add(one_platform)
            if col == "*":
                one_coin = Coins(x, y)
                all_coins.add(one_coin)
                all_sprites.add(one_coin)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

def create_objects():
    create_platforms()
    create_player()
    create_mobs()
    create_sword(player)

def handle_events():
    # ивент выхода
    for event in pygame.event.get():
        # выход из программы
        if event.type == pygame.QUIT:
            global running
            running = False
        # ивенты движения (остановка на всякий случай)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.stop()
        # ивенты удара
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player.sword.make_sword()

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        #     player.sword.down_sword()
        # if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
        #     player.sword.up_sword()

    # ивенты движения
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player.go_lef()
    if keystate[pygame.K_RIGHT]:
        player.go_right()
    if keystate[pygame.K_UP]:
        player.go_jump()
    if keystate[pygame.K_DOWN]:
        player.go_down()
        # player.up_sword()
    if keystate[pygame.K_SPACE]:
        if player.sword_exist:
            player.remove_sword()
        # else:
        #     create_sword(player)

# Цикл игры
create_objects()
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    handle_events()

    # ОБНОВЛЕНИЕ
    all_sprites.update()

    # РЕНДЕРИНГ
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()