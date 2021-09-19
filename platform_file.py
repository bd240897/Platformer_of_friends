import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(pygame.Color(PLATFORM_COLOR))
        # self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        ground_img = pygame.image.load(os.path.join(img_dir, "ground_1.png")).convert()
        ground_img = pygame.transform.scale(ground_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        ground_img.set_colorkey(WHITE)
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.orig_rect = self.rect.copy()

