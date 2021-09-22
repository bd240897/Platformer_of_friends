import numpy as np
import os
import pygame

# размер платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

WIDTH_WINDOW = PLATFORM_WIDTH*25
HEIGHT_WINDOW = PLATFORM_HEIGHT*21

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


########################################################################################################################
"Уровень"

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

level_2 = [
    "---------------------------------",
    "                                -",
    "-                               -",
    "-                               -",
    "-       -------------------------",
    "-                               -",
    "--                              -",
    "----                   *        -",
    "---------------------------     -",
    "---                             -",
    "--                              -",
    "-               -----------------",
    "-                               -",
    "-           *                   -",
    "-       ------                  -",
    "--                              -",
    "----   *      *                 -",
    "---------------           -------",
    "----                 -          -",
    "--               -       -     *-",
    "-                            ----",
    "-                      -       --",
    "-                    ---        -",
    "-*                 -----         ",
    "---------------------------------",
    "---------------------------------"]

level = [
    "---------------------------------",
    "-                               -",
    "-                               -",
    "-                               -",
    "-            --                 -",
    "-                               -",
    "--                              -",
    "-                               -",
    "-                   ---         -",
    "-                               -",
    "-                               -",
    "-      ---                      -",
    "-    *      *          -        -",
    "-   --- --------                -",
    "-                               -",
    "-                -   *          -",
    "-                   --          -",
    "-                               -",
    "- *                  *          -",
    "---------------------------------",
    "---------------------------------"]

TOTAL_LEVEL_WEIGHT = len(level_2[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
TOTAL_LEVEL_HEIGHT = len(level_2) * PLATFORM_HEIGHT  # высоту

point_spawn_player_1 = (WIDTH_WINDOW/2, HEIGHT_WINDOW - 50 - 2*PLATFORM_HEIGHT)
point_spawn_player_2 = (TOTAL_LEVEL_WEIGHT//2, PLATFORM_HEIGHT*3)

##############################################################################################################################
"""Размеры других спрайтов"""

# размер монет
SIZE_OF_COIN = 10
# размер мобов
MOB_SIZE = PLATFORM_WIDTH

# размер персонажа
PLAYER_HEIGHT = PLATFORM_WIDTH
PLAYER_WIDTH = int(PLATFORM_HEIGHT*1.5)

# количество мобов
COUNT_MOBS = 3

# положение меча
SWORD_SHIFT_X = 10
SWORD_SHIFT_Y = 42

# цифровая карта платформы
def get_map_platform(level):
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
    return level_digit, num_blok_x, num_blok_y

level_digit, num_blok_x, num_blok_y = get_map_platform(level_2)


########################################################################################################################
"""Изображения"""
img_dir = os.path.join(os.path.dirname(__file__), 'img')
snd_dir = os.path.join(os.path.dirname(__file__), 'snd')
BACKGROUND = pygame.image.load(os.path.join(img_dir, "plan_1.png"))