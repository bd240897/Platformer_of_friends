# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 800
HEIGHT = 680
FPS = 30
GRAVITY = 4

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# уровень
level = [
    "-------------------------",
    "-                       -",
    "-                       -",
    "-                       -",
    "-            --         -",
    "-                       -",
    "--                      -",
    "-                       -",
    "-                   --- -",
    "-                       -",
    "-                       -",
    "-      ---              -",
    "-                       -",
    "-   -----------        -",
    "-                       -",
    "-                -      -",
    "-                   --  -",
    "-                       -",
    "-                       -",
    "-------------------------"]

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # отрисуем персонажа
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # поля персонажа
        self.x = 0
        self.y = 0
        self.speed_x = None
        self.speed_y = None
        self.onGround = False
        self.rect.centerx = WIDTH / 2 # базовое расположение
        self.rect.bottom = HEIGHT - 50 - 2*PLATFORM_HEIGHT

    def update(self):
        # перемещение по Х
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        self.rect.x += self.speed_x

        # перемещение по Y
        self.speed_y = 0
        if keystate[pygame.K_UP]:
            self.speed_y = -8
        if keystate[pygame.K_DOWN]:
            self.speed_y = 8
        self.rect.y += self.speed_y

        if not self.onGround:
            self.speed_y += GRAVITY
        self.onGround = False

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(pygame.Color(PLATFORM_COLOR))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


bloks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# рисование уровня
x = y = 0  # координаты
for row in level:  # вся строка
    for col in row:  # каждый символ
        if col == "-":
            one_platform = Platform(x, y)
            bloks.add(one_platform)
            all_sprites.add(one_platform)
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
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        #     left = True
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        #     right = True
        # if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
        #     right = False
        # if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
        #     left = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        #     up = True
        # if event.type == pygame.KEYUP and event.key == pygame.K_UP:
        #     up = False



##### ОБНОВЛЕНИЕ
    all_sprites.update()

##### РЕНДЕРИНГ
    # проверка столкновений с платформами
    hits = pygame.sprite.spritecollide(player, bloks, False)
    for hit in hits:
        if player.speed_x > 0:
            # hit.rect.right = player.rect.left
            player.rect.right = hit.rect.left
        if player.speed_x < 0:
            # hit.rect.left = player.rect.right
            player.rect.left = hit.rect.right
        if player.speed_y > 0:
            # hit.rect.bottom = player.rect.top
            player.rect.bottom = hit.rect.top
        if player.speed_y < 0:
            # hit.rect.top = player.rect.bottom
            player.rect.top = hit.rect.bottom
            # player.onGround = True

    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()