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

Resources:
python 3.9 documentation: https://docs.python.org/3.9/
pygame documentation: https://www.pygame.org/docs/
"""
from modules.gui import GUI
from modules.gui import colours
from modules.input import InputHandler
from modules.playfield import Playfield
from modules.timer import Timer

import pygame


def main():
    """
    Initiate Conway's Game Of Life (GoL).

    Proxy to the game logic.
    """
    # define window size and initialize GUI class
    window_size = window_width, window_height = 1280, 840
    gui = GUI("Conway's Game Of Life", window_size, 60)

    # setup playfield to with and height given
    playfield_size = playfield_width, playfield_height = 20, 20
    playfield = Playfield(playfield_size, window_size)

    # initialize the handler for input and the timer
    timer = Timer()
    handler = InputHandler()

    # setting up game loop
    _skip = False
    while handler.running():
        # take loop start time and poll for input
        _skip = timer.poll(gui.frame_limit)
        result = handler.poll()

        if not _skip:
            # flush window and surface
            gui.flush()
            playfield.flush_surface()

        # define UI buttons
        button_clear = gui.add_button('Clear', colours.white, window_height + 10, 60)
        button_random = gui.add_button('Random', colours.white, window_height + 10, 110)

        # handle left button click
        if handler.button_pressed() and not handler.locked() and result.event_button == 1:
            handler.lock()
            # set / unset single cells
            if 0 < result.event_x < (playfield_width * playfield.cell_size) and\
                    0 < result.event_y < (playfield_height * playfield.cell_size):
                cell_x = result.event_x // playfield.cell_size
                cell_y = result.event_y // playfield.cell_size
                playfield.flip_cell(cell_x, cell_y)
            # menu clear
            if button_clear.bottom_x > result.event_x > button_clear.top_x and\
                    button_clear.bottom_y > result.event_y > button_clear.top_y:
                playfield.clear()
            # menu random
            if button_random.bottom_x > result.event_x > button_random.top_x and\
                    button_random.bottom_y > result.event_y > button_random.top_y:
                playfield.randomize()

        # handle right button click, i.e. simulate (one mouseclick equals one generation change)
        if handler.button_pressed() and not handler.locked() and result.event_button == 3:
            handler.lock()
            playfield.simulate()

        if not _skip:
            # drawing playfield
            playfield.update_surface()
            gui.add_surface(playfield.surface, (10, 10))

            # output fps
            gui.add_button(f'FPS: {(1 // timer.last_frame_time() )}', colours.white, window_height + 10, 10)

            # flip screen buffer
            pygame.display.flip()


if __name__ == '__main__':
    main()
