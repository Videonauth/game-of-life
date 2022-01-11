#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game_of_life.py
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 06.01.22 - 13:40
# Purpose: Using pygame library to create a version of conways game of life
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""
Conways Game of Life.

Task:
Create Conways game of life with help of pygame library.

Rules:
The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is
in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts
with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.
At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

1. Any live cell with two or three live neighbours survives.
2. Any dead cell with three live neighbours becomes a live cell.
3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules
simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously, and the
discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of
the preceding one. The rules continue to be applied repeatedly to create further generations.

Goals:
- have logging
- have an initial set state, by user choice.
- have a proper game loop with error checking and error states.
- have an option for the game to be run for x amount of frames until it ends, or have it run until user interrupt.
- have an FPS limiter.
- have a resizable window.
- have an option to choose the playing field size
- have full screen swap option
- have mouse and keyboard input

Resources:
python 3.9 documentation: https://docs.python.org/3.9/
pygame documentation: https://www.pygame.org/docs/
"""
import time

from modules.colour import Colour
from modules.playfield import generate_playfield
from modules.playfield import generate_seeded_playfield
from modules.simulation import simulation

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
        pygame.display.flip()

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
        pygame.draw.rect(surface, colour, (2, 2, width - 4, height - 4), 1)
        self.window.blit(surface, (top_x, top_y))
        return top_x, top_y, top_x + width, top_y + height


class Playfield:
    pass


def main():
    """
    Initiate Conway's Game Of Life (GoL).

    Proxy to the game logic.
    """
    # initialize colour class
    colour = Colour()

    # define window size and initialize GUI
    window_size = width, height = 1280, 840
    gui = GUI("Conway's Game Of Life", window_size, 60)
    gui.flush()

    # setup surface
    playfield_surface = pygame.Surface((height - 20, height - 20))
    menu_surface = pygame.Surface((width - height, height))

    # pre-draw menu surface
    pygame.draw.rect(menu_surface, colour.white, (10, 10, width - height - 20, height - 20), 1)
    pygame.draw.line(menu_surface, colour.white, (10, 40), (width - height - 10, 40), 1)
    pygame.draw.line(menu_surface, colour.white, (10, 45), (width - height - 10, 45), 1)
    text = gui.font.render('Clear', True, colour.white)
    button_clear_abs_position = (height + 10, 45, width - 10, 65)
    menu_surface.blit(text, (20, 50))
    pygame.draw.line(menu_surface, colour.white, (10, 65), (width - height - 10, 65), 1)
    pygame.draw.line(menu_surface, colour.white, (10, 70), (width - height - 10, 70), 1)
    text = gui.font.render('Random Seed', True, colour.white)
    button_random_abs_position = (height + 10, 70, width - 10, 90)
    menu_surface.blit(text, (20, 75))
    pygame.draw.line(menu_surface, colour.white, (10, 90), (width - height - 10, 90), 1)
    pygame.draw.line(menu_surface, colour.white, (10, 95), (width - height - 10, 95), 1)

    # setup playfield to with and height given
    playfield_width = 20
    playfield_height = 20
    playfield = generate_playfield(playfield_height, playfield_width)

    # setting up game loop
    _last_frame_time = 0
    _running = True
    cell_size = (height - 20) // max(playfield_width, playfield_height)
    mouse_x = 0
    mouse_y = 0
    button = 0
    _locked = False
    _pressed = False
    while _running:
        _t = time.time()

        # event handling for input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and not _pressed:
                mouse_x, mouse_y = event.pos
                button = event.button
                _pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                _locked = False
                _pressed = False

        # flush window and surface
        gui.window.fill(colour.black)
        playfield_surface.fill(colour.black)

        # set or unset single cells on mouseclick
        if _pressed and not _locked and button == 1:
            # set / unset
            if mouse_x < (playfield_width * cell_size) and mouse_y < (playfield_height * cell_size):
                cell_x = mouse_x // cell_size
                cell_y = mouse_y // cell_size
                playfield[cell_y][cell_x] = playfield[cell_y][cell_x] ^ 1
            # menu clear
            if button_clear_abs_position[2] > mouse_x > button_clear_abs_position[0]:
                if button_clear_abs_position[3] > mouse_y > button_clear_abs_position[1]:
                    playfield = generate_playfield(playfield_height, playfield_width)
            # menu random
            if button_random_abs_position[2] > mouse_x > button_random_abs_position[0]:
                if button_random_abs_position[3] > mouse_y > button_random_abs_position[1]:
                    playfield = generate_seeded_playfield(playfield_height,
                                                          playfield_width,
                                                          int(playfield_height * playfield_width * 0.5))
            _locked = True

        # simulate (one mouseclick equals one generation change)
        if _pressed and not _locked and button == 3:
            _locked = True
            playfield = simulation(playfield)

        # drawing playfield
        start_x = 0
        start_y = 0
        for line in playfield:
            for cell in line:
                if cell == 0:
                    pygame.draw.rect(playfield_surface, colour.white, (start_x, start_y, cell_size, cell_size), 1)
                elif cell == 1:
                    pygame.draw.rect(playfield_surface, colour.blue, (start_x, start_y, cell_size, cell_size))
                    pygame.draw.rect(playfield_surface, colour.white, (start_x, start_y, cell_size, cell_size), 1)
                else:
                    pass
                start_x += cell_size
            start_x = 0
            start_y += cell_size

        gui.window.blit(playfield_surface, (10, 10))
        gui.window.blit(menu_surface, (height + 1, 0))

        # output fps
        if _last_frame_time != 0:
            text = gui.font.render(f'FPS: {1 / _last_frame_time}', True, colour.white)
            gui.window.blit(text, (height + 20, 20))

        # wait when to fast
        while time.time() - _t < gui.frame_limit:
            pass

        # calculate frame time
        _t_stop = time.time()
        _last_frame_time = _t_stop - _t

        # flip screen buffer
        pygame.display.flip()

# s        # skip frames if needed
# s        if last_frame_time > 1/fps_limit:
# s            last_frame_time = time.time() - _frame_start_t
# s            continue


if __name__ == '__main__':
    main()