import numpy as np
import os
import pygame

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
PURPUR = (152, 0, 136)
GRAY = (230, 230, 230)

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
    "-    *      *          -",
    "-   --- --------        -",
    "-                       -",
    "-                -   *  -",
    "-                   --  -",
    "-                       -",
    "- *                  *  -",
    "-------------------------",
    "-------------------------"]

# размер платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
# размер монет
SIZE_OF_COIN = 10
# размер мобов
MOB_SIZE = PLATFORM_WIDTH

# размер персонажа
PLAYER_HEIGHT = PLATFORM_WIDTH
PLAYER_WIDTH = int(PLATFORM_HEIGHT*1.5)


# цифровая карта платформы
x = y = 0  # координаты
num_blok_y = len(level[0])
num_blok_x = len(level)
level_digit = [[0 for i in range(num_blok_y)] for j in range(num_blok_x)]

for i, row in enumerate(level):  # вся строка
    for j, col in enumerate(row):  # каждый символ
        if col == "-":
            level_digit[i][j] = (x,y)
        else:
            level_digit[i][j] = (0, 0)
        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
    y += PLATFORM_HEIGHT  # то же самое и с высотой
    x = 0  # на каждой новой строчке начинаем с нуля


img_dir = os.path.join(os.path.dirname(__file__), 'img')

SWORD_SHIFT_X = 10
SWORD_SHIFT_Y = 42

