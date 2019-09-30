from utils import (  # COLORS & FONTS
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    FONT_DROID)
from utils import (  # KINECT
    KINECT,
    KINECT_EVENT_STREAM,
    KINECT_FRAME_SIZE,
    NEW_BODY_FRAME_EVENT,
    NEW_BODY_INDEX_FRAME_EVENT)
from utils import (  # PYGAME
    CORRECT_ANSWER,
    INCORRECT_ANSWER,
    render_player,
    SCREEN,
    SCREEN_SIZE,
    Size)

from pykinect2 import PyKinectV2
import pygame
import random

from components.text import Text

INCR = 20
# CHAR_SIZE = Size(FONT_DROID.size(' '))
CHAR_SIZE = Size((28, 54))
LAST_X = 0


class Game_2:
    def __init__(self):
        self.bg = pygame.image.load('game_2/game_2.jpg')
        self.probability_of_good_char = 0.3  # Probability of next character being good
        self.margin_row = 20

        self.chars_on_screen = []
        self.good_chars_on_screen_count = 0
        self.frame = 0

        self.target_size = 20
        self.player_size = Size(
            int(KINECT_FRAME_SIZE.W / 1.5),
            int(KINECT_FRAME_SIZE.H / 1.5))

        self.body_frame = None
        self.body_index_frame = None

        KINECT_EVENT_STREAM.subscribe(self.event_handler)

    def event_handler(self, e):
        if e.type == NEW_BODY_FRAME_EVENT:
            self.body_frame = e.body_frame
        elif e.type == NEW_BODY_INDEX_FRAME_EVENT:
            self.body_index_frame = e.body_index_frame

    def check_collisions(self):
        for body in self.body_frame.bodies:
            if not body.is_tracked:
                continue
            joints = body.joints
            jointPoints = KINECT.body_joints_to_depth_space(joints)

            hand_left = jointPoints[PyKinectV2.JointType_HandLeft]
            hand_right = jointPoints[PyKinectV2.JointType_HandRight]

            target_left = pygame.draw.circle(
                SCREEN,
                COLOR_BLUE, (
                    int(hand_left.x * self.player_size.W / KINECT_FRAME_SIZE.W + (SCREEN_SIZE.W - self.player_size.W) / 2),
                    int(hand_left.y * self.player_size.H / KINECT_FRAME_SIZE.H + SCREEN_SIZE.H - self.player_size.H)),
                self.target_size)
            target_right = pygame.draw.circle(
                SCREEN,
                COLOR_BLUE, (
                    int(hand_right.x * self.player_size.W / KINECT_FRAME_SIZE.W + (SCREEN_SIZE.W - self.player_size.W) / 2),
                    int(hand_right.y * self.player_size.H / KINECT_FRAME_SIZE.H + SCREEN_SIZE.H - self.player_size.H)),
                self.target_size)

            for char in self.chars_on_screen:
                if char.collide(target_left) or char.collide(target_right):
                    if char.is_good:
                        CORRECT_ANSWER.play()
                    else:
                        INCORRECT_ANSWER.play()

    def render(self):
        SCREEN.blit(pygame.transform.scale(self.bg, (SCREEN_SIZE.W, SCREEN_SIZE.H)), (0, 0))

        bad_chars = list('BCDFGHJKLMNPQRSTVWXYZ')
        good_chars = list('AEIOU')
        next_char_at = (self.margin_row + CHAR_SIZE.H) / INCR

        self.frame += 1
        if self.frame % next_char_at == 0:
            if random.random() <= self.probability_of_good_char:
                char = Char(random.choice(good_chars), is_good=True)
            else:
                char = Char(random.choice(bad_chars), is_good=False)
            self.chars_on_screen.append(char)

        if self.body_index_frame is not None:
            for char in self.chars_on_screen:
                char.render()

            self.check_collisions()
            render_player(
                self.body_index_frame,
                self.player_size,
                'bottom center')

            self.chars_on_screen = [
                char for char in self.chars_on_screen if char.fresh]

        pygame.display.update()


class Char:
    def __init__(self, char, is_good):
        global LAST_X

        self.fresh = True
        self.is_good = is_good
        if self.is_good:
            self.text = Text(char, size=40, color=COLOR_GREEN)
        else:
            self.text = Text(char, size=40, color=COLOR_RED)

        margin_edge = SCREEN_SIZE.W / 4
        self.rect = self.text.surface.get_rect()
        self.rect.x = random.randint(margin_edge, SCREEN_SIZE.W - CHAR_SIZE.W - margin_edge)
        while abs(self.rect.x - LAST_X) < 50:
            self.rect.x = random.randint(margin_edge, SCREEN_SIZE.W - CHAR_SIZE.W - margin_edge)
        LAST_X = self.rect.x
        self.rect.y = -CHAR_SIZE.H

    def collide(self, rect):
        did_collide = self.rect.colliderect(rect)
        if did_collide:
            self.fresh = False
        return did_collide

    def move(self):
        self.rect.y += INCR
        if self.rect.y >= SCREEN_SIZE.H:
            self.fresh = False

    def render(self):
        self.move()
        self.text.render(self.rect)
