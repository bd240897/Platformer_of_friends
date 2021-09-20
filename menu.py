import pygame
from constants import *
import sys

class Menu(pygame.sprite.Sprite):

    def quit(self):
        self.done = False

    def continue_loop(self):
        sys.exit()

    def print_conole(self):
        print('кнопка_3')
        self.done = False

    def run_help(self):
        pass

    def HELP_back(self):
        print('Бэк')
        self.__init__()
        self.create_menu()
        self.draw()
        self.update(self.screen)
        self.handler_menu_events()

    def run_help(self):
        self.__init__()
        self.create_help()
        self.draw()
        self.update(self.screen)
        self.handler_help_events()

    button_1 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 5, u"1. Продолжить", WHITE, quit]
    button_2 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 9, u"2. Справка", WHITE, run_help]
    button_3 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 13, u"3. Выйти из игры", WHITE, continue_loop]
    LIST_BUTTONS = [button_1, button_2, button_3]

    HELP = [u'CПРАВКА',
              u'< - движение влево',
              u'> - движение вправо',
              u'^ - прыжок',
              u'Q - достать мечь слева',
              u'P - достать мечь справа',
              u'SPACE - удар',
              u'НАЗАД']

    LIST_HELP = []
    for i, support in enumerate(HELP):
        color = WHITE
        click_handler = lambda x: None
        if i == 0:
            color = BLUE
        if i == len(HELP)-1:
            click_handler = HELP_back
            color = RED
        one_support = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * (2 + i*2), support, color, click_handler]
        LIST_HELP.append(one_support)


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TOTAL_LEVEL_WEIGHT, TOTAL_LEVEL_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.objects = []
        self.done = True

    def create_menu(self):
        self.objects.clear()
        for button in self.LIST_BUTTONS:
            coord = (button[0], button[1])
            text = button[2]
            size = 50
            color = button[3]
            handler_click = button[4]
            button = Button(text, size, *coord, color, handler_click)
            self.objects.append(button)

    def create_help(self):
        self.objects.clear()
        for button in self.LIST_HELP:
            coord = (button[0], button[1])
            text = button[2]
            size = 50
            color = button[3]
            handler_click = button[4]
            button = Button(text, size, *coord, color, handler_click)
            self.objects.append(button)

    def draw(self):
        for obj in self.objects:
            obj.draw(self.image)

    def update(self, screen):
        screen.blit(self.image, (0,0))
        pygame.display.flip()

    def run(self, screen):
        self.screen = screen
        self.create_menu()
        self.draw()
        self.update(screen)
        self.handler_menu_events()

    def handler_menu_events(self):
        while self.done:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # перебирваем все кнопки
                for active_button in self.objects:
                    # проверяем есть ли пересечение
                    collide_button = active_button.rect.collidepoint(mouse)
                    if collide_button:
                        # делаем все кнопки БЕЛЫЕ
                        for btn in self.LIST_BUTTONS:
                            btn[3] = WHITE
                        # изменяем цвет выборанной кнопки ЧЕРНУЮ
                        index = self.objects.index(active_button)
                        self.LIST_BUTTONS[index][3] = BLACK
                        self.create_menu()
                        self.draw()
                        self.update(self.screen)
                        # проверяем нажата ли кнопка
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            active_button.click_handler(self)

    def handler_help_events(self):
        while self.done:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                for active_button in self.objects:
                    # проверяем есть ли пересечение
                    collide_button = active_button.rect.collidepoint(mouse)
                    if collide_button:
                        # подкрашивание выделеного элемента
                        last_element = len(self.HELP)-1
                        current_element = self.objects.index(active_button)
                        if current_element == len(self.objects) - 1:
                            self.LIST_HELP[last_element][3] = BLACK
                        else:
                            self.LIST_HELP[last_element][3] = RED
                        self.create_help()
                        self.draw()
                        self.update(self.screen)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            active_button.click_handler(self)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, x, y, color, click_handler):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.text = text
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        self.image = font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.click_handler = click_handler

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        pass
    
    