# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from player_file import *
from constants import *
from coin_file import *
from mobs_file import *
import random

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# cоздаим группы и добави туда объекты
all_bloks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_coins = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()

player = Player(all_bloks, all_coins, all_mobs)

########### УБРАТЬ
sword = Sword()
sword.rect.center = player.rect.topleft
sw_image = sword.image
angle = 0
###########

all_sprites.add(sword)
# player.get_sword(sword)


all_sprites.add(player)
for num_mob in range(1,4):
    mob = Mob(*Mob.random_mob_position(), all_bloks)
    all_mobs.add(mob)
    all_sprites.add(mob)

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




# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

##### ОБНОВЛЕНИЕ
    all_sprites.update()

    # перемещение
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player.go_lef()
    if keystate[pygame.K_RIGHT]:
        player.go_right()
    if keystate[pygame.K_UP]:
        player.go_jump()
    if keystate[pygame.K_DOWN]:
        player.go_down()
        ########### УБРАТЬ
        # player.make_sword()
        angle += 1
        angle = angle % 360
        sword.image = pygame.transform.rotate(sw_image, angle)
        sword.rect = sword.image.get_rect()
        sword.rect.center = player.rect.topleft

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and player.speed_x < 0:
            player.stop()
        if event.key == pygame.K_RIGHT and player.speed_x > 0:
            player.stop()

##### РЕНДЕРИНГ
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()