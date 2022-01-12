[![Python Version 3.8](assets/github/python-3.8.svg)](https://docs.python.org/3.8/index.html)
[![Python Version 3.9](assets/github/python-3.9.svg)](https://docs.python.org/3.9/index.html)

# Conways Game of Life.

## Task:
Create Conways game of life with help of pygame library.

## Rules:
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
([source: wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules))

## Goals:
- not looking at other peoples code or solutions for it
- have logging
- have an initial set state, by user choice.
- have a proper game loop with error checking and error states.
- have an option for the game to be run for x amount of frames until it ends, or have it run until user interrupt.
- have an FPS limiter.
- have a resizable window.
- have an option to choose the playing field size
- have full screen swap option
- have mouse and keyboard input

## Resources:
[python 3.8 documentation](https://docs.python.org/3.8/index.html) <br>
[python 3.9 documentation](https://docs.python.org/3.9/index.html) <br>
[pygame documentation](https://www.pygame.org/docs/)

## Usage
User Action | Result
--- | ---
left click on the grid | set / unset cell
left click on clear | clear the playfield
left click on random | fill the playfield with random seed
right click anywhere | simulate one generation step
