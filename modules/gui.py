#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - gui
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 11.01.22 - 22:55
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""GUI class."""
from collections import namedtuple
from typing import Tuple

from modules.colour import Colour

import pygame

# initialize colour class
colours = Colour()

Button = namedtuple('Button', ['label',
                               'colour',
                               'left',
                               'top',
                               'right',
                               'bottom',
                               'surface',
                               'hover_surface',
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


class GUI:
    """GUI class contains everything belonging to output and the window."""

    def __init__(self, caption: str, window_size: Tuple[int, int], fps: int):
        """Initialize the graphical user interface."""
        # storing window dimensions for internal use
        self._window_size = window_size
        self._window_width = window_size[0]
        self._window_height = window_size[1]
        # calculate frame limit storing outward facing
        self.frame_limit = 1 / fps
        # init pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        # create and name window
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(caption)
        # setup default flush colour
        self._flush_colour = colours.black
        # setup font
        self.font = pygame.font.SysFont('Arial', 20, False, False)

    def flush(self):
        """Fill the whole window output screen with a chosen colour."""
        # flush output
        self.window.fill(self._flush_colour)

    def add_button(self,
                   label: str,
                   colour: Tuple[int, int, int] = colours.black,
                   left: int = 0,
                   top: int = 0,
                   width: int = 420,
                   height: int = 40,
                   background_image: pygame.Surface = None,
                   background_colour: Tuple[int, int, int] = None,
                   hover_colour: Tuple[int, int, int] = None,
                   ):
        """Draw a button on the output screen and return the clickable border positions absolute."""
        _surface = pygame.Surface((width, height))
        _surface_hover = pygame.Surface((width, height))
        # fill if we got a colour we fill the button with it
        if background_colour is not None:
            _surface.fill(background_colour)
        # draw an image if we got one
        if background_image is not None:
            _surface.blit(background_image, (0, 0))
        # draw the inner and outer border
        pygame.draw.rect(_surface, colour, (0, 0, width, height), 1)
        pygame.draw.rect(_surface, colour, (3, 3, width - 6, height - 6), 1)
        # render the text centered
        text = self.font.render(label, True, colour)
        _text_boundary = text.get_rect()
        _surface.blit(text, ((width / 2) - (_text_boundary.width / 2), (height / 2) - (_text_boundary.height / 2)))
        # draw and return tuple for clickable surface positions
        self.window.blit(_surface, (left, top))
        # draw the hover image or make a copy of the normal surface
        if hover_colour is not None:
            _surface_hover.fill(hover_colour)
            pygame.draw.rect(_surface_hover, colour, (0, 0, width, height), 1)
            pygame.draw.rect(_surface_hover, colour, (3, 3, width - 6, height - 6), 1)
            _surface_hover.blit(text, ((width / 2) - (_text_boundary.width / 2),
                                       (height / 2) - (_text_boundary.height / 2)))
        else:
            _surface_hover.blit(_surface, (0, 0))
        return Button(label, colour, left, top, left + width, top + height, _surface, _surface_hover)

    def add_surface(self, surface: pygame.Surface, pos_abs: Tuple[int, int]):
        """Draw a surface onto the internal window class."""
        self.window.blit(surface, pos_abs)

    def add_text(self, label: str, pos_abs: Tuple[int, int], colour):
        """Draw a string to screen at position."""
        text = self.font.render(label, True, colour)
        self.window.blit(text, pos_abs)
        return text

    def add_rectangle(self, left: int = 0, top: int = 0, width: int = 10, height: int = 10,
                      colour: Tuple[int, int, int] = colours.black):
        """"Draw a rectangle on the screen."""
        _surface = pygame.Surface((width, height))
        pygame.draw.rect(_surface, colour, (0, 0, width, height), 1)
        self.window.blit(_surface, (left, top))
