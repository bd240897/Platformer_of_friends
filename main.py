# Pygame шаблон - скелет для нового проекта Pygame
import pygame
from player_file import Player
from coin_file import Coins
from mobs_file import Mob
from platform_file import Platform
from sword_file import Sword
from constants import *
from menu import Menu

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# cоздаим группы и добави туда объекты
all_bloks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_coins = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()

CAMER_SIZE = (100,100)

class Camera(object):
    def __init__(self, camera_func, width_level, height_level):
        self.camera_func = camera_func
        self.rect_level = pygame.Rect(0, 0, width_level, height_level)

    def apply(self, obj):
        return obj.rect.move(self.rect_level.topleft)

    def update(self, player):
        self.rect_level = self.camera_func(self.rect_level, player.rect)


def camera_configure(rect_level, player_rect):
    # создаем прямоугольник с центром у персе и размером с игровой экран
    l, t, _, _ = player_rect
    _, _, w, h = rect_level
    l, t = -l + WIDTH_WINDOW/2, -t + HEIGHT_WINDOW/2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(rect_level.width - WIDTH_WINDOW), l)  # Не движемся дальше правой границы
    t = max(-(rect_level.height - HEIGHT_WINDOW), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


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
    player.create_sword(sword)
    all_sprites.add(sword)

def create_platforms():
    # рисование уровня
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                one_platform = Platform(x,y)
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
    create_player()
    create_platforms()
    create_mobs()

def handle_events():
    # ивенты НАЖАТИЙ
    for event in pygame.event.get():
        # выход из программы
        if event.type == pygame.QUIT:
            global running
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            m = Menu()
            m.draw(screen)

        # ивенты движения (остановка на всякий случай)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.stop()

        # ивенты удара и доставания меча
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            sword_side = 'left'
            if player.sword_exist:
                player.remove_sword()
            else:
                create_sword(player)
                player.take_sword(sword_side)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            sword_side = 'right'
            if player.sword_exist:
                player.remove_sword()
            else:
                create_sword(player)
                player.take_sword(sword_side)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.make_sword()

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

# Цикл игры
camera = Camera(camera_configure, TOTAL_LEVEL_WEIGHT, TOTAL_LEVEL_HEIGHT)
create_objects()
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    handle_events()

    # ОБНОВЛЕНИЕ
    screen.fill(BLACK)
    background = pygame.image.load(os.path.join(img_dir, "plan_1.png")).convert()
    background = pygame.transform.scale(background, (WIDTH_WINDOW, HEIGHT_WINDOW))
    background_rect = background.get_rect()
    screen.blit(background, background_rect)

    camera.update(player)  # центризируем камеру относительно персонажа
    for sprites in all_sprites:
        screen.blit(sprites.image, camera.apply(sprites))
        sprites.update()

    # all_sprites.update()

    # РЕНДЕРИНГ
    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()