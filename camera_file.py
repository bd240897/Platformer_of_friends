from constants import *


class Camera(object):
    def __init__(self, camera_func, width_level, height_level):
        self.camera_func = camera_func
        self.rect_level = pygame.Rect(0, 0, width_level, height_level)

    def apply(self, obj):
        return obj.rect.move(self.rect_level.topleft)

    def update(self, player):
        self.rect_level = self.camera_func(self.rect_level, player.rect)

    @staticmethod
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
