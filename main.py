from utils import (
    ACTIVE,
    EVENT_STREAM,
    KINECT,
    POST_NEW_BODY_FRAME_EVENT,
    POST_NEW_BODY_INDEX_FRAME_EVENT,
    SCREEN,
    SCREEN_SIZE)

import pygame

from game_1.game_1 import Game_1
from game_2.game_2 import Game_2
from game_3.game_3 import Game_3
from menu.menu import Menu
from components.pause_screen import PauseScreen


class Astrocytes:
    def __init__(self):
        pygame.display.set_caption('Astrocytes')
        self.background = pygame.Surface((SCREEN_SIZE.W, SCREEN_SIZE.H))
        ACTIVE.append('menu')

        self.menu = Menu()
        self.pause_screen = PauseScreen()
        self.game_1 = Game_1()
        self.game_2 = Game_2()
        self.game_3 = Game_3()

        EVENT_STREAM.subscribe(self.event_handler)

    def event_handler(self, e):
        self.check_pause(e)
        self.check_exit(e)

    def check_pause(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if ACTIVE[-1] == 'pause-screen':
                    self.pause_screen.hide()
                    ACTIVE.pop()
                else:
                    ACTIVE.append('pause-screen')

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            for e in pygame.event.get():
                EVENT_STREAM.on_next(e)

            if ACTIVE[-1] == 'menu':
                self.menu.render()

            elif ACTIVE[-1] == 'game_1':
                if KINECT.has_new_body_frame():
                    POST_NEW_BODY_FRAME_EVENT(
                        body_frame=KINECT.get_last_body_frame())

                if KINECT.has_new_body_index_frame():
                    POST_NEW_BODY_INDEX_FRAME_EVENT(
                        body_index_frame=KINECT.get_last_body_index_frame())

                self.game_1.render()

            elif ACTIVE[-1] == 'game_2':
                if KINECT.has_new_body_frame():
                    POST_NEW_BODY_FRAME_EVENT(
                        body_frame=KINECT.get_last_body_frame())

                if KINECT.has_new_body_index_frame():
                    POST_NEW_BODY_INDEX_FRAME_EVENT(
                        body_index_frame=KINECT.get_last_body_index_frame())

                self.game_2.render()

            elif ACTIVE[-1] == 'game_3':
                if KINECT.has_new_body_frame():
                    POST_NEW_BODY_FRAME_EVENT(
                        body_frame=KINECT.get_last_body_frame())

                if KINECT.has_new_body_index_frame():
                    POST_NEW_BODY_INDEX_FRAME_EVENT(
                        body_index_frame=KINECT.get_last_body_index_frame())
                self.game_3.render()

            elif ACTIVE[-1] == 'pause-screen':
                self.pause_screen.render()

            pygame.display.update()

    def check_exit(self, e):
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif (e.type == pygame.KEYDOWN):
            if e.key == pygame.K_F4:
                if bool(e.mod & pygame.KMOD_ALT):
                    pygame.quit()
                    quit()


if __name__ == '__main__':
    game = Astrocytes()
    game.run()
