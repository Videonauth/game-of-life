#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - gui
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 20.01.22 - 23:40
# Purpose: -
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""Window and GUI class live here."""
from collections import namedtuple
from typing import Tuple

from modules.colour import Colour

import pygame


colours = Colour()


Button = namedtuple('Button', ['label',
                               'left',
                               'top',
                               'right',
                               'bottom',
                               'width',
                               'height',
                               'colour',
                               'hover_colour',
                               'background_colour',
                               'surface',
                               'hover',
                               ])


def point_is_within_bounds(bound_x_min: int,
                           bound_x_max: int,
                           bound_y_min: int,
                           bound_y_max: int,
                           point_x: int,
                           point_y: int,
                           ) -> bool:
    """Check whether a point exists within the given rectangular bounds."""
    return (bound_x_min < point_x < bound_x_max) and (bound_y_min < point_y < bound_y_max)


class Window:
    """Window class."""

    def __init__(self, caption: str, window_size: Tuple[int, int], fps: int = 60):
        """Initialize the Window class."""
        if not pygame.get_init():
            pygame.init()
        self.size = window_size
        self.frame_limit = 1 / fps
        self.surface = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)
        self.background_colour = colours.bg_grey
        self.stroke_colour = colours.light_grey
        self.font = pygame.font.SysFont('Arial', 20, False, False)

    def set_stroke_colour(self, colour: Tuple[int, int, int]):
        """Set the line colour."""
        self.stroke_colour = colour

    def set_background_colour(self, colour: Tuple[int, int, int]):
        """Set the background colour."""
        self.background_colour = colour

    @staticmethod
    def flip():
        """Flip the screen buffer."""
        pygame.display.flip()


class GUI:
    """GUI class."""

    def __init__(self, window: Window):
        """Initialize the GUI class."""
        self.window = window

    def fill(self, colour: Tuple[int, int, int] = None):
        """Fill the screen with a colour."""
        if colour is not None:
            self.window.surface.fill(colour)
        else:
            self.window.surface.fill(self.window.background_colour)

    def line(self, left: int, top: int, right: int, bottom: int, colour: Tuple[int, int, int]):
        """Draw a line on the screen."""
        pygame.draw.line(self.window.surface, colour, (left, top), (right, bottom))

    def rectangle(self, left: int, top: int, width: int, height: int, colour: Tuple[int, int, int]):
        """Draw a rectangle to the screen."""
        pygame.draw.rect(self.window.surface, colour, (left, top, left + width, top + height))

    def text(self, label: str, left: int, top: int, colour: Tuple[int, int, int]):
        """Output text on the screen."""
        text = self.window.font.render(label, True, colour)
        self.window.surface.blit(text, (left, top))

    def surface(self, surface: pygame.Surface, left: int, top: int):
        """Add a surface on the screen."""
        self.window.surface.blit(surface, (left, top))

    def button(self,
               label: str,
               left: int,
               top: int,
               width: int = 420,
               height: int = 40,
               colour: Tuple[int, int, int] = None,
               hover_colour: Tuple[int, int, int] = None,
               background_colour: Tuple[int, int, int] = None,
               ):
        """Define a Button and render it initially."""
        _surface = pygame.Surface((width, height))
        _hover = pygame.Surface((width, height))
        if background_colour is not None:
            _surface.fill(background_colour)
        else:
            _surface.fill(self.window.background_colour)
        if hover_colour is not None:
            _hover.fill(hover_colour)
        else:
            _hover.fill(self.window.background_colour)
        if colour is not None:
            text = self.window.font.render(label, True, colour)
            _text_boundary = text.get_rect()
            pygame.draw.rect(_surface, colour, (0, 0, width, height), 1)
            pygame.draw.rect(_surface, colour, (3, 3, width - 6, height - 6), 1)
            _surface.blit(text, ((width / 2) - (_text_boundary.width / 2), (height / 2) - (_text_boundary.height / 2)))
            self.window.surface.blit(_surface, (left, top))
            pygame.draw.rect(_hover, colour, (0, 0, width, height), 1)
            pygame.draw.rect(_hover, colour, (3, 3, width - 6, height - 6), 1)
        else:
            text = self.window.font.render(label, True, self.window.stroke_colour)
            _text_boundary = text.get_rect()
            pygame.draw.rect(_surface, self.window.stroke_colour, (0, 0, width, height), 1)
            pygame.draw.rect(_surface, self.window.stroke_colour, (3, 3, width - 6, height - 6), 1)
            _surface.blit(text, ((width / 2) - (_text_boundary.width / 2), (height / 2) - (_text_boundary.height / 2)))
            self.window.surface.blit(_surface, (left, top))
            pygame.draw.rect(_hover, self.window.stroke_colour, (0, 0, width, height), 1)
            pygame.draw.rect(_hover, self.window.stroke_colour, (3, 3, width - 6, height - 6), 1)
        return Button(label, left, top, left + width, top + height, width, height,
                      colour, hover_colour, background_colour, _surface, _hover)
