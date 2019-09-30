from utils import (
    ACTIVE,
    COLOR_BLACK,
    COLOR_WHITE,
    FONT_ROBOTO,
    SCREEN,
    SCREEN_SIZE)

import pygame

from components.button import Button
from components.text import Text


def quit_game():
    pygame.quit()
    quit()


class PauseScreen:
    def __init__(self):
        self.hidden = True
        self.width = 0
        self.max_witdh = 200

        self.init_buttons()

    def init_buttons(self):
        self.btn_back = Button(
            'pause-screen',
            (self.max_witdh, 50),
            bg=(80, 80, 80),
            fg=(50, 50, 50),
            text=Text('Back', color=COLOR_WHITE),
            on_left_click=self.load_prev)

        self.btn_menu = Button(
            'pause-screen',
            (self.max_witdh, 50),
            bg=(80, 80, 80),
            fg=(50, 50, 50),
            text=Text('Main Menu', color=COLOR_WHITE),
            on_left_click=self.load_menu)

        self.btn_quit = Button(
            'pause-screen',
            (self.max_witdh, 50),
            bg=(80, 80, 80),
            fg=(50, 50, 50),
            text=Text('Quit', color=COLOR_WHITE),
            on_left_click=quit_game)

    def hide(self):
        self.width = 0
        self.hidden = True

    def load_menu(self):
        self.hide()
        ACTIVE.append('menu')

    def load_prev(self):
        self.hide()
        ACTIVE.pop()

    def render(self):
        if self.hidden:
            tint = pygame.Surface(
                (SCREEN_SIZE.W, SCREEN_SIZE.H),
                pygame.SRCALPHA)
            tint.fill((0, 0, 0, 150))
            SCREEN.blit(tint, (0, 0))
            self.hidden = False

        SCREEN.fill(
            (100, 100, 100),
            (SCREEN_SIZE.W - self.width, 0, self.width, SCREEN_SIZE.H))

        self.btn_back.render((SCREEN_SIZE.W - self.width, 0))
        self.btn_menu.render((SCREEN_SIZE.W - self.width, 50))
        self.btn_quit.render((SCREEN_SIZE.W - self.width, 100))

        if self.width < self.max_witdh:
            self.width += 50
