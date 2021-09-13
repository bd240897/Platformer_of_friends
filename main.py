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
        self.speed_x = 0
        self.speed_y = 0
        self.onGround = False
        self.rect.centerx = WIDTH / 2 # базовое расположение
        self.rect.bottom = HEIGHT - 50 - 2*PLATFORM_HEIGHT

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
        platform_hit_list = pygame.sprite.spritecollide(self, bloks, False)
        self.rect.y -= 2

        # Если все в порядке, прыгаем вверх
        if len(platform_hit_list) > 0:
            self.onGround = True

    def update(self):
        self.onGround = False
        self.check_onGraound()

        if not self.onGround:
            if self.speed_y == 0:
                self.speed_y = 1
            else:
                self.speed_y += 1
        # print(self.speed_y)

        # self.rect.x += self.speed_x
        # self.rect.y += self.speed_y

        # проверка столкновений с платформами
        # hits = pygame.sprite.spritecollide(self, bloks, False)
        # for hit in hits:
        #     print(self.rect.bottomleft[1] > hit.rect.top, self.rect.bottomright[1] > hit.rect.top, ' @ ', \
        #     self.rect.topright[0] > hit.rect.left, self.rect.bottomright[0] > hit.rect.left)
        #
        #     if self.speed_y > 0 and (self.rect.bottomleft[1] > hit.rect.top) and (self.rect.bottomright[1] > hit.rect.top):
        #         self.rect.bottom = hit.rect.top
        #     elif self.speed_y < 0 and (self.rect.topleft[1] < hit.rect.bottom) and (self.rect.topright[1] < hit.rect.bottom):
        #         self.rect.top = hit.rect.bottom
        #     self.speed_y = 0
        #
        # for hit in hits:
        #     if self.speed_x > 0 and (self.rect.topright[0] > hit.rect.left) and (self.rect.bottomright[0] > hit.rect.left):
        #         self.rect.right = hit.rect.left
        #     elif self.speed_x < 0 and (self.rect.topleft[0] < hit.rect.right) and (self.rect.bottomleft[0] < hit.rect.right):
        #         self.rect.left = hit.rect.right
        #     self.speed_x = 0

        self.rect.x += self.speed_x
        hits = pygame.sprite.spritecollide(self, bloks, False)
        for hit in hits:
            if self.speed_x > 0:
                self.rect.right = hit.rect.left
            elif self.speed_x < 0:
                self.rect.left = hit.rect.right
            self.speed_x = 0

        self.rect.y += self.speed_y
        hits = pygame.sprite.spritecollide(self, bloks, False)
        for hit in hits:
            if self.speed_y > 0:
                self.rect.bottom = hit.rect.top
            elif self.speed_y < 0:
                self.rect.top = hit.rect.bottom
            self.speed_y = 0
        #





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

##### ОБНОВЛЕНИЕ
    all_sprites.update()

    # перемещение по Х
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        player.go_lef()
    if keystate[pygame.K_RIGHT]:
        player.go_right()
    if keystate[pygame.K_UP]:
        player.go_jump()
    if keystate[pygame.K_DOWN]:
        player.go_down()

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