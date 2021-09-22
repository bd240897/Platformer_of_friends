import pygame
from constants import *
import sys
import os

class Menu(pygame.sprite.Sprite):
    def __init__(self, screen, color = GREEN):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface((TOTAL_LEVEL_WEIGHT, TOTAL_LEVEL_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.objects = []
        self.done = True
        self.sounds_play = False
########################################################################################################################
    '''handlers для кнопок'''

    def quit(self):
        """Функция выходы из меню - handler для кнопки"""
        self.done = False

    def continue_loop(self):
        """Функция выходы из игры - handler для кнопки"""
        sys.exit()

    def HELP_back(self):
        self.__init__(self.screen)
        self.create(self.LIST_MENU_BUTTONS)
        self.draw()
        self.update()
        self.handler_menu_events()

    # изучили декаратор в классе
    def _run_help_decarator(run_help):
        def temp(self):
            run_help(self)
            self.draw()
            self.update()
            self.handler_help_events()
        return temp

    @_run_help_decarator
    def run_help(self):
        self.__init__(self.screen)
        self.create(self.LIST_HELP)
        # self.draw()
        # self.update()
        # self.handler_help_events()

########################################################################################################################
    '''Входные данные'''

    button_1 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 5, u"1. Продолжить", WHITE, quit]
    button_2 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 9, u"2. Справка", WHITE, run_help]
    button_3 = [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 13, u"3. Выйти из игры", WHITE, continue_loop]
    LIST_MENU_BUTTONS = [button_1, button_2, button_3]

    HELP = [u'CПРАВКА',
              u'← - движение влево',
              u'→ - движение вправо',
              u'↑ - прыжок',
              u'Q - достать мечь слева',
              u'P - достать мечь справа',
              u'SPACE - удар',
              u'ВЕРНУТЬСЯ НАЗАД']

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

    LIST_BEGIN_TEXT = [
    [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 6, u"ИГРА: \"No NAME GAME\"", BLUE, lambda x: None, 70],
    [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 10, u"Написал: Борисов Д.А.", WHITE, lambda x: None, 50],
    [PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 16, u"Нажмите любю кнопку для продолжения", RED, lambda x: None, 40]]

    LIST_WIN_TEXT = [[PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 9, u'YOU WIN', RED, lambda x: None, 90]]
    LIST_GAME_OVER_TEXT = [[PLATFORM_WIDTH * 12, PLATFORM_WIDTH * 9, u'YOU DIED', RED, lambda x: None, 90]]

########################################################################################################################
    '''Запускаторы и креаторы'''

    def run_menu_outside(self):
        """Первый запуск меню из main"""
        self.create(self.LIST_MENU_BUTTONS)
        self.draw()
        self.update()
        self.handler_menu_events()

    def run_begin_screen(self):
        """Отображение первоначального окна"""
        status = "begin_window"
        self.__init__(self.screen)
        self.create(self.LIST_BEGIN_TEXT)
        background = BACKGROUND.convert()
        background = pygame.transform.scale(BACKGROUND, (WIDTH_WINDOW, HEIGHT_WINDOW))
        background_rect = background.get_rect()
        self.image.blit(background, background_rect)
        self.draw()
        self.update()
        self.handler_begin_screen_events(status="begin_window")

    def run_end_game(self, status):
        pygame.mixer.init()
        sounds_you_win = pygame.mixer.Sound(os.path.join(snd_dir, 'you_win_2.wav'))
        sounds_you_lose = pygame.mixer.Sound(os.path.join(snd_dir, 'you_lose.wav'))
        """Отображение оконо победы и поражения"""
        if status == 'lose_game':
            self.__init__(self.screen, color=BLACK)
            self.create(self.LIST_GAME_OVER_TEXT)
            sounds_you_lose.play()
        elif status == 'win_game':
            self.__init__(self.screen, color=BLUE)
            self.create(self.LIST_WIN_TEXT)
            sounds_you_win.play()
        self.draw()
        self.update()
        self.handler_begin_screen_events(status)

    def create(self, LIST_OF_TEXT):
        """Креатор окон - расоложения надписей"""
        self.objects.clear()
        for button in LIST_OF_TEXT:
            coord = (button[0], button[1])
            text = button[2]
            if len(LIST_OF_TEXT[0])-1 > 4:
                size = button[5]
            else:
                size = 50
            color = button[3]
            handler_click = button[4]
            button = Button(text, size, *coord, color, handler_click)
            self.objects.append(button)

########################################################################################################################
    '''Обработчики событий'''

    def handler_menu_events(self):
        """Обработчик меню"""
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
                        for btn in self.LIST_MENU_BUTTONS:
                            btn[3] = WHITE
                        # изменяем цвет выборанной кнопки ЧЕРНУЮ
                        index = self.objects.index(active_button)
                        self.LIST_MENU_BUTTONS[index][3] = BLACK
                        self.create(self.LIST_MENU_BUTTONS)
                        self.draw()
                        self.update()
                        # проверяем нажата ли кнопка
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            active_button.click_handler(self)

    def handler_help_events(self):
        """Обработчик помощь"""
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
                        self.create(self.LIST_HELP)
                        self.draw()
                        self.update()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            active_button.click_handler(self)


    def handler_begin_screen_events(self, status = None):
        """Обработчик первого окна"""
        count_play = 0
        time_make = 0
        sounds_make_sword = pygame.mixer.Sound(os.path.join(snd_dir, 'make_sword_2.wav'))

        while self.done:
            # звуки ударов меча в начале
            if status == 'begin_window':
                curtime = pygame.time.get_ticks()
                if count_play < 3 and curtime - time_make >= 700:
                    sounds_make_sword.play()
                    count_play += 1
                    time_make = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if status in ['lose_game', 'win_game'] and event.type == pygame.KEYDOWN:
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.done = False

    def draw(self):
        for obj in self.objects:
            obj.draw(self.image)

    def update(self):
        self.screen.blit(self.image, (0,0))
        pygame.display.flip()

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