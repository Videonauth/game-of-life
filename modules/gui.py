#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - gui
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 11.01.22 - 22:55
# Purpose: -
# Written for: Python 3.6.3
# ---------------------------------------------------------------------------

"""gui class."""

import pygame


class GUI:
    """Lorem ipsum dolor sit amet ..."""

    def __init__(self, caption: str, window_size: tuple, fps: int):
        """Ipsum dolor lorem sit amet ..."""
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
        # setup font
        self.font = pygame.font.SysFont(None, 20, False, False)

    def flush(self):
        """Dolor ipsum lorem sit amet ..."""
        # flush output
        self.window.fill((0, 0, 0))

    def add_button(self,
                   label: str,
                   colour: tuple = (255, 255, 255),
                   top_x: int = 0,
                   top_y: int = 0,
                   width: int = 420,
                   height: int = 40,
                   background_image: str = '',
                   background_colour: tuple = (-1, -1, -1)
                   ) -> tuple:
        """implicate that there are docstrings outside ..."""
        surface = pygame.Surface((width, height))
        if not background_colour == (-1, -1, -1):
            surface.fill(background_colour)
        if not background_image == '':
            # fixme: image should not be loaded in a function which might be called in the game loop
            _image = pygame.image.load(background_image)
            # todo: insert image bound check
            surface.blit(_image, (0, 0))
        # draw the button
        pygame.draw.rect(surface, colour, (0, 0, width, height), 1)
        pygame.draw.rect(surface, colour, (3, 3, width - 6, height - 6), 1)
        text = self.font.render(label, True, colour)
        _text_boundary = text.get_rect()
        surface.blit(text, ((width / 2) - (_text_boundary.width / 2), (height / 2) - (_text_boundary.height / 2)))
        self.window.blit(surface, (top_x, top_y))
        return top_x, top_y, top_x + width, top_y + height


if __name__ == '__main__':
    pass
