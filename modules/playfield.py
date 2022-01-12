#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Playfield factories and manipulation."""

from collections import namedtuple
from random import sample
from typing import List, Tuple

from modules.gui import colours
from modules.simulation import simulation

import pygame


def generate_playfield(_playfield_height: int, _playfield_width: int) -> List[List[int]]:
    """
    Create a matrix from lists, with the specified height and width.

    int _playfield_width : matrix size in x direction
    int _playfield_height : matrix size in y direction
    return : list[list[], ...] as a matrix
    """
    if _playfield_height <= 0 or _playfield_width <= 0:
        raise ValueError('Height and width must be positive')

    if _playfield_height == 1 and _playfield_width == 1:
        raise ValueError('At least one dimension must be greater than one')

    return [[0 for _ in range(_playfield_width)] for __ in range(_playfield_height)]


Cell = namedtuple('Cell', ['row', 'cell'])


def serialize_playfield(_playfield: List[List[int]]) -> str:
    """Create a string representation of the playfield."""
    _max_width = 3
    _field = []
    if not isinstance(_playfield, list):
        raise ValueError('_playfield is not a list')
    for _row in _playfield:
        if not isinstance(_row, list):
            raise ValueError('_playfield is not a list of lists')
        _field.append(''.join([str(_cell).ljust(_max_width) for _cell in _row]).strip())

    return '\n'.join(_field)


def generate_seeded_playfield(
    _playfield_height: int,
    _playfield_width: int,
    _number_of_seeded_cells: int,
) -> List[List[int]]:
    """Create a seeded playfield."""
    # Create an initial playfield
    _playfield = generate_playfield(_playfield_height, _playfield_width)

    # Cast to int to be sure
    _number_of_seeded_cells = int(_number_of_seeded_cells)

    # Validate the _number_of_seeded_cells input
    _playfield_size = _playfield_height * _playfield_width
    if _number_of_seeded_cells < 0:
        raise ValueError(f'_number_of_seeded_cells too small: must be in the range [0, {_playfield_size}]')

    if _number_of_seeded_cells > (_playfield_height * _playfield_width):
        raise ValueError(f'_number_of_seeded_cells too large: must be in the range [0, {_playfield_size}]')

    # Determine and activate a random sample of cells
    _full_set = [Cell(row, cell) for row in range(_playfield_height) for cell in range(_playfield_width)]
    _cells_to_seed = sample(_full_set, _number_of_seeded_cells)
    for _cell_to_seed in _cells_to_seed:
        _playfield[_cell_to_seed.row][_cell_to_seed.cell] = 1

    return _playfield


class Playfield:
    """Playfield class contains everything done in regard of the playfield."""

    def __init__(self,
                 playfield_size: Tuple[int, int],
                 surface_size: Tuple[int, int],
                 ):
        """Initialize the playfield class."""
        self.width = playfield_size[0]
        self.height = playfield_size[1]
        self._flush_colour = colours.black
        if not pygame.get_init():
            pygame.init()
        self.surface = pygame.Surface((min(surface_size[0], surface_size[1]) - 20,
                                       min(surface_size[0], surface_size[1]) - 20))
        self.field = generate_playfield(self.height, self.width)
        self.cell_size = (min(surface_size[0], surface_size[1]) - 20) // max(self.width, self.height)

    def flush_surface(self):
        """Flush the output surface."""
        self.surface.fill(self._flush_colour)

    def flip_cell(self, cell_x, cell_y):
        """Flip a playfield cell from set to unset and vice versa."""
        self.field[cell_y][cell_x] = self.field[cell_y][cell_x] ^ 1

    def clear(self):
        """Clear the playfield, i.e. setting each cell to zero."""
        self.field = generate_playfield(self.height, self.width)

    def randomize(self, multiplier: float = 0.5):
        """Fill the playfield with randomized cells."""
        self.field = generate_seeded_playfield(self.height, self.width, int(self.height * self.width * multiplier))

    def simulate(self):
        """Simulate one generation step on the playfield."""
        self.field = simulation(self.field)

    def update_surface(self):
        """Draw the actual playfield onto the output surface."""
        # drawing playfield
        start_x = 0
        start_y = 0
        for line in self.field:
            for cell in line:
                if cell == 0:
                    pygame.draw.rect(self.surface, colours.white, (start_x, start_y, self.cell_size, self.cell_size), 1)
                elif cell == 1:
                    pygame.draw.rect(self.surface, colours.blue, (start_x, start_y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.surface, colours.white, (start_x, start_y, self.cell_size, self.cell_size), 1)
                else:
                    pass
                start_x += self.cell_size
            start_x = 0
            start_y += self.cell_size
