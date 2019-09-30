from rx.subjects import Subject
import ctypes
import numpy as np
import pygame

from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


pygame.init()


class Size:
    def __init__(self, w, h=None):
        if isinstance(w, tuple):
            (w, h) = w
        self.W = self.width = w
        self.H = self.height = h


# GLOBAL CONSTANTS
KINECT = PyKinectRuntime.PyKinectRuntime(
    PyKinectV2.FrameSourceTypes_Body |
    PyKinectV2.FrameSourceTypes_Color |
    PyKinectV2.FrameSourceTypes_BodyIndex)

EVENT_STREAM = Subject()
KINECT_EVENT_STREAM = Subject()

SCREEN_SIZE = Size(512, 384)
SCREEN = pygame.display.set_mode(
    (SCREEN_SIZE.W, SCREEN_SIZE.H),
    pygame.DOUBLEBUF | pygame.HWSURFACE)

KINECT_FRAME_SIZE = Size(
    KINECT.body_index_frame_desc.Width,
    KINECT.body_index_frame_desc.Height)
PLAYER = pygame.Surface(
    (KINECT_FRAME_SIZE.W, KINECT_FRAME_SIZE.H),
    0,
    32).convert_alpha()

NEW_BODY_FRAME_EVENT = 1 + pygame.USEREVENT
NEW_BODY_INDEX_FRAME_EVENT = 2 + pygame.USEREVENT


# GLOBAL VARIABLES
ACTIVE = []


# COLORS
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)


# FONTS
FONT_ROBOTO = 'fonts/roboto/Roboto-Regular.ttf'
FONT_DROID = 'fonts/Droid_Sans/DroidSans-Bold.ttf'


# SOUNDS
CORRECT_ANSWER = pygame.mixer.Sound('correct_answer.wav')
INCORRECT_ANSWER = pygame.mixer.Sound('incorrect_answer.wav')


# HELPER FUNCTIONS
def POST_EVENT(event_type, **event_data):
    e = pygame.event.Event(event_type, event_data)
    EVENT_STREAM.on_next(e)


def POST_NEW_BODY_FRAME_EVENT(**event_data):
    e = pygame.event.Event(NEW_BODY_FRAME_EVENT, event_data)
    KINECT_EVENT_STREAM.on_next(e)


def POST_NEW_BODY_INDEX_FRAME_EVENT(**event_data):
    e = pygame.event.Event(NEW_BODY_INDEX_FRAME_EVENT, event_data)
    KINECT_EVENT_STREAM.on_next(e)


def render_player(frame, size, position):
    hide = (frame == 255)
    show = (frame != 255)

    frame[hide] = 0
    frame[show] = 255

    frame = np.array((frame, frame, frame, frame))
    (r, g, b, a) = frame
    r[r == 255] = 100
    frame = np.ravel(frame.T)

    PLAYER.lock()
    address = KINECT.surface_as_array(PLAYER.get_buffer())
    ctypes.memmove(address, frame.ctypes.data, frame.size)
    del address
    PLAYER.unlock()

    (w, h) = (SCREEN_SIZE.W, SCREEN_SIZE.H)
    pos_rect = pygame.Rect((0, 0), (size.W, size.H))
    if isinstance(position, tuple):
        pos_rect.topleft = position
    elif isinstance(position, str):
        if position == 'top left':
            pos_rect.topleft = (0, 0)
        if position == 'top center':
            pos_rect.midtop = (w / 2, 0)
        if position == 'top right':
            pos_rect.topright = (w, 0)

        if position == 'center left':
            pos_rect.midleft = (0, h / 2)
        if position == 'center center':
            pos_rect.center = (w / 2, h / 2)
        if position == 'center right':
            pos_rect.midleft = (w, h / 2)

        if position == 'bottom left':
            pos_rect.bottomleft = (0, h)
        if position == 'bottom center':
            pos_rect.midbottom = (w / 2, h)
        if position == 'bottom right':
            pos_rect.bottomright = (w, h)

    SCREEN.blit(pygame.transform.scale(PLAYER, (size.W, size.H)), pos_rect)
