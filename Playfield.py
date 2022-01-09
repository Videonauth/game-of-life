#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Playfield factories and manipulation."""

from collections import namedtuple
from random import sample
from typing import List


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
    for _row in _playfield:
        _field.append(''.join([str(_cell).ljust(_max_width) for _cell in _row]))

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
