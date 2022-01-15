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
                   top_x: int = 0,
                   top_y: int = 0,
                   width: int = 420,
                   height: int = 40,
                   background_image: pygame.Surface = None,
                   background_colour: Tuple[int, int, int] = None,
                   ):
        """Draw a button on the output screen and return the clickable border positions absolute."""
        _surface = pygame.Surface((width, height))
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
        self.window.blit(_surface, (top_x, top_y))

        ReturnValue = namedtuple('ReturnValue', ['label', 'colour', 'top_x', 'top_y', 'bottom_x', 'bottom_y'])
        return ReturnValue(label, colour, top_x, top_y, top_x + width, top_y + height)

    def add_surface(self, surface: pygame.Surface, pos_abs: Tuple[int, int]):
        """Draw a surface onto the internal window class."""
        self.window.blit(surface, pos_abs)


if __name__ == '__main__':
    pass
