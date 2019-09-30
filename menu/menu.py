from utils import (
    ACTIVE,
    COLOR_GREEN,
    SCREEN,
    SCREEN_SIZE)

import pygame

from components.button import Button
from components.text import Text


def load_game(idx):
    ACTIVE.append('game_%d' % (idx))
    print 'GAME %d LOADED' % (idx)


class Menu:
    def __init__(self):
        self.bg = pygame.transform.scale(
            pygame.image.load('menu/menu.png'),
            (SCREEN_SIZE.W, SCREEN_SIZE.H))

        self.init_buttons()

    def init_buttons(self):
        self.game = Button('menu', (
                (305 / 1024.0) * SCREEN_SIZE.W,
                (305 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g.png'),
            fg=pygame.image.load('menu/gf.png'),
            on_left_click=lambda: load_game(1)
        )

        self.btn_1 = Button('menu', (
                (143 / 1024.0) * SCREEN_SIZE.W,
                (143 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g1.png'),
            fg=pygame.image.load('menu/g1f.png'),
            text=Text('Game 1'),
            on_left_click=lambda: load_game(1)
        )

        self.btn_2 = Button('menu', (
                (143 / 1024.0) * SCREEN_SIZE.W,
                (143 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g2.png'),
            fg=pygame.image.load('menu/g2f.png'),
            text=Text('Game 2'),
            on_left_click=lambda: load_game(2)
        )

        self.btn_3 = Button('menu', (
                (143 / 1024.0) * SCREEN_SIZE.W,
                (143 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g3.png'),
            fg=pygame.image.load('menu/g3f.png'),
            text=Text('Game 3'),
            on_left_click=lambda: load_game(3)
        )

        self.btn_4 = Button('menu', (
                (143 / 1024.0) * SCREEN_SIZE.W,
                (143 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g4.png'),
            fg=pygame.image.load('menu/g4f.png'),
            text=Text('Game 4')
        )

        self.btn_5 = Button('menu', (
                (143 / 1024.0) * SCREEN_SIZE.W,
                (143 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/g5.png'),
            fg=pygame.image.load('menu/g5f.png'),
            text=Text('Game 5')
        )

        self.profile = Button('menu', (
                (467 / 1024.0) * SCREEN_SIZE.W,
                (92 / 768.0) * SCREEN_SIZE.H),
            bg=pygame.image.load('menu/p.png'),
            fg=pygame.image.load('menu/pf.png'),
            text=Text('VIEW MY PROFILE')
        )

    def render(self):
        SCREEN.blit(self.bg, (0, 0))

        self.game.render((
            (22 / 1024.0) * SCREEN_SIZE.W,
            (94 / 768.0) * SCREEN_SIZE.H))
        self.btn_1.render((
            (345 / 1024.0) * SCREEN_SIZE.W,
            (94 / 768.0) * SCREEN_SIZE.H))
        self.btn_2.render((
            (345 / 1024.0) * SCREEN_SIZE.W,
            (257 / 768.0) * SCREEN_SIZE.H))
        self.btn_3.render((
            (345 / 1024.0) * SCREEN_SIZE.W,
            (420 / 768.0) * SCREEN_SIZE.H))
        self.btn_4.render((
            (184 / 1024.0) * SCREEN_SIZE.W,
            (420 / 768.0) * SCREEN_SIZE.H))
        self.btn_5.render((
            (22 / 1024.0) * SCREEN_SIZE.W,
            (420 / 768.0) * SCREEN_SIZE.H))
        self.profile.render((
            (22 / 1024.0) * SCREEN_SIZE.W,
            (582 / 768.0) * SCREEN_SIZE.H))
