import pygame
from constants import *
import sys

class Menu(pygame.sprite.Sprite):

    button_1 = (PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 4, u"1. Продолжить")
    button_2 = (PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 8, u"2. Выйти из игры")
    list_buttons = [button_1, button_2]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TOTAL_LEVEL_WEIGHT, TOTAL_LEVEL_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.all_buttons = []
        self.done = True

    def draw(self):
        for button in self.list_buttons:
            coord = (button[0], button[1])
            text = button[2]
            size = 50
            button = Button(text, size, *coord, color=WHITE)
            self.all_buttons.append(button)
            self.image.blit(button.image, button.rect)

    def draw_one_button(self, button, color=WHITE):
        coord = (button[0], button[1])
        text = button[2]
        size = 50
        button = Button(text, size, *coord, color)
        self.all_buttons.append(button)
        self.image.blit(button.image, button.rect)

    def run_menu(self, screen):
        self.screen = screen
        # self.draw()
        for button in self.list_buttons:
            self.draw_one_button(button)
        screen.blit(self.image, (0,0))
        pygame.display.flip()
        self.main_loop()

    def main_loop(self):
        while self.done:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                for active_button in self.all_buttons:
                    if active_button.rect.collidepoint(mouse) > 0 and active_button == self.all_buttons[0]:
                        self.draw_one_button(self.list_buttons[0], color=BLACK)
                        self.draw_one_button(self.list_buttons[1], color=WHITE)
                        self.screen.blit(self.image, (0, 0))
                        pygame.display.flip()
                        print('1')
                    elif active_button.rect.collidepoint(mouse) > 0 and active_button == self.all_buttons[1]:
                        self.draw_one_button(self.list_buttons[0], color=WHITE)
                        self.draw_one_button(self.list_buttons[1], color=BLACK)
                        self.screen.blit(self.image, (0, 0))
                        pygame.display.flip()
                        print('2')

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for active_button in self.all_buttons:
                        if active_button.rect.collidepoint(mouse) > 0 and active_button == self.all_buttons[0]:
                            self.done = False
                        elif active_button.rect.collidepoint(mouse) > 0 and active_button == self.all_buttons[1]:
                            sys.exit()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.text = text
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        self.image = font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
