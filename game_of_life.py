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
from modules.gui import Window
from modules.gui import colours
from modules.gui import point_is_within_bounds
from modules.input import InputHandler
from modules.playfield import Playfield
from modules.timer import Timer


def main():
    """
    Initiate Conway's Game Of Life (GoL).

    Proxy to the game logic.
    """
    # define window size and initialize GUI class
    window_size = window_width, window_height = 1280, 840
    window = Window("Conway's Game of Life", window_size, 60)
    gui = GUI(window)

    # setup playfield to with and height given
    playfield_size = 20, 20
    playfield = Playfield(playfield_size, window_size)

    # initialize the handler for input and the timer
    timer = Timer()
    handler = InputHandler()

    # define UI buttons
    button_list = [gui.button(label='Clear',
                              left=window_height + 10,
                              top=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='Random',
                              left=window_height + 10,
                              top=110,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='% +',
                              left=window_height + 10,
                              top=160,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='% -',
                              left=window_width - 70,
                              top=160,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='x +',
                              left=window_height + 10,
                              top=210,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='x -',
                              left=window_width - 70,
                              top=210,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='y +',
                              left=window_height + 10,
                              top=260,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey),
                   gui.button(label='y -',
                              left=window_width - 70,
                              top=260,
                              width=60,
                              colour=window.stroke_colour,
                              hover_colour=colours.medium_grey)]

    # setting up game loop
    _random = 0.5
    while handler.running():
        # poll for input
        result = handler.poll()

        # handle left button clicks
        if handler.button_pressed() and not handler.locked() and result.event_button == 1:
            handler.lock()
            # set / unset single cells
            if point_is_within_bounds(0, playfield.width * playfield.cell_size,
                                      0, playfield.height * playfield.cell_size,
                                      result.event_x, result.event_y):
                cell_x = result.event_x // playfield.cell_size
                cell_y = result.event_y // playfield.cell_size
                playfield.flip_cell(cell_x, cell_y)
            # process all buttons for input actions
            _current = playfield.get_size()
            for button in button_list:
                if point_is_within_bounds(button.left, button.right,
                                          button.top, button.bottom,
                                          result.event_x, result.event_y):
                    if button.label == 'Clear':
                        playfield.clear()

                    if button.label == 'Random':
                        playfield.randomize(_random)

                    if button.label == '% +':
                        if _random * 100 < 100:
                            _random += 0.01

                    if button.label == '% -':
                        if _random * 100 > 0:
                            _random -= 0.01

                    if button.label == 'x +':
                        playfield.resize(_current.width + 1, _current.height)

                    if button.label == 'x -':
                        playfield.resize(_current.width - 1, _current.height)

                    if button.label == 'y +':
                        playfield.resize(_current.width, _current.height + 1)

                    if button.label == 'y -':
                        playfield.resize(_current.width, _current.height - 1)

        # handle right button clicks, i.e. simulate (one mouseclick equals one generation change)
        if handler.button_pressed() and not handler.locked() and result.event_button == 3:
            handler.lock()
            playfield.simulate()

        if not timer.poll(window.frame_limit):
            # flush window and surface
            gui.fill()
            playfield.flush_surface()

            # draw buttons
            for button in button_list:

                if point_is_within_bounds(button.left, button.right,
                                          button.top, button.bottom,
                                          result.x, result.y):
                    gui.surface(button.hover, button.left, button.top)
                else:
                    gui.surface(button.surface, button.left, button.top)

            # drawing playfield
            playfield.update_surface()
            gui.surface(playfield.surface, 10, 10)

            gui.button(label=f'Random: %:{int(_random * 100)}',
                       left=window_height + 80,
                       top=160,
                       width=280,
                       colour=window.stroke_colour)

            gui.button(label=f'Playfield: x: {playfield.width} y: {playfield.height}',
                       left=window_height + 80,
                       top=210,
                       width=280,
                       height=90,
                       colour=window.stroke_colour)
            # output fps
            gui.button(label=f'FPS: {(1 // timer.last_frame_time() )}',
                       left=window_height + 10,
                       top=10,
                       colour=window.stroke_colour)

            # flip screen buffer
            window.flip()


if __name__ == '__main__':
    main()
