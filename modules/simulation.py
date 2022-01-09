#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - simulation
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 09.01.22 - 23:39
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""Conways game of life simulation function."""


def simulation(playfield: list) -> list:
    """Simulate a playfield for one generation step."""
    _playfield_height = len(playfield)
    _playfield_width = len(playfield[0])
    new_playfield = []
    for _line in range(_playfield_height):
        _new_line = []
        for _cell in range(_playfield_width):
            _cell_current = playfield[_line][_cell]
            _neighbours = 0

            # evaluate neighbours if existent/possible
            if not _line - 1 < 0 and not _cell - 1 < 0:
                _neighbours += playfield[_line - 1][_cell - 1]
            if not _line - 1 < 0 and not _cell < 0:
                _neighbours += playfield[_line - 1][_cell]
            if not _line - 1 < 0 and not _cell + 1 > _playfield_width - 1:
                _neighbours += playfield[_line - 1][_cell + 1]
            if not _line < 0 and not _cell - 1 < 0:
                _neighbours += playfield[_line][_cell - 1]
            if not _line < 0 and not _cell + 1 > _playfield_width - 1:
                _neighbours += playfield[_line][_cell + 1]
            if not _line + 1 > _playfield_height - 1 and not _cell - 1 < 0:
                _neighbours += playfield[_line + 1][_cell - 1]
            if not _line + 1 > _playfield_height - 1 and not _cell < 0:
                _neighbours += playfield[_line + 1][_cell]
            if not _line + 1 > _playfield_height - 1 and not _cell + 1 > _playfield_width - 1:
                _neighbours += playfield[_line + 1][_cell + 1]

            # evaluate cell survival
            if _cell_current == 1 and _neighbours < 2:
                cell_out = 0
            elif _cell_current == 1 and _neighbours > 3:
                cell_out = 0
            elif _cell_current == 0 and _neighbours == 3:
                cell_out = 1
            else:
                cell_out = _cell_current
            _new_line.append(cell_out)
        new_playfield.append(_new_line)
    return new_playfield


if __name__ == '__main__':
    pass
