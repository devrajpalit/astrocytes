from utils import (
    ACTIVE,
    EVENT_STREAM,
    SCREEN)

import pygame


class Button:
    def __init__(self, context, (w, h), bg, fg=None, text=None, on_left_click=None, on_middle_click=None, on_right_click=None):
        self.context = context

        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

        self.bg = bg
        self.fg = fg or bg
        self.text = text

        self.left_click_callback = on_left_click
        self.middle_click_callback = on_middle_click
        self.right_click_callback = on_right_click

        self.is_focused = False

        EVENT_STREAM.subscribe(self.event_handler)

    def event_handler(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.on_click(e)
        elif e.type == pygame.MOUSEMOTION:
            if self.focused(e):
                self.is_focused = True
            else:
                self.is_focused = False

    def focused(self, e):
        if ACTIVE[-1] != self.context:
            return False

        return (
            (self.x < e.pos[0] and e.pos[0] < self.x + self.w) and
            (self.y < e.pos[1] and e.pos[1] < self.y + self.h))

    def on_click(self, e):
        if ACTIVE[-1] != self.context:
            return

        if (
            (self.x < e.pos[0] and e.pos[0] < self.x + self.w) and
            (self.y < e.pos[1] and e.pos[1] < self.y + self.h)
        ):
            if e.button == 1:
                if self.left_click_callback:
                    self.left_click_callback()

            elif e.button == 2:
                if self.middle_click_callback:
                    self.middle_click_callback()

            elif e.button == 3:
                if self.right_click_callback:
                    self.right_click_callback()

    def render(self, pos):
        (self.x, self.y) = pos

        if self.is_focused:
            icon = self.fg
        else:
            icon = self.bg

        if isinstance(icon, pygame.Surface):
            surface = pygame.transform.scale(icon, (int(self.w), int(self.h)))
            surface_rect = surface.get_rect()
            surface_rect.topleft = (self.x, self.y)
            surface_rect.bottomright = (self.x + self.w, self.y + self.h)

            SCREEN.blit(surface, surface_rect)

        elif isinstance(icon, tuple):
            surface_rect = pygame.draw.rect(SCREEN, icon, (self.x, self.y, self.w, self.h))

        if self.text:
            self.text.render(surface_rect)
