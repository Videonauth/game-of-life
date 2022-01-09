#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Testsuite for generate_playfield."""

from Playfield import generate_playfield

import pytest


class TestPlayingFieldFactory:
    """Testsuite for generate_playfield factory."""

    @pytest.mark.parametrize('_height,_width', [[0, 1], [1, 0], [-1, 1], [1, -2], [0, 0]])
    def test_non_positive_numbers_yield_exceptions(self, _height, _width):
        """Non-positive arguments yield ValueError."""
        with pytest.raises(ValueError):
            generate_playfield(_height, _width)

    def test_exception_raised_if_both_dimensions_are_one(self):
        """Value error yielded if both dimensions have magnitude one."""
        _height = 1
        _width = 1
        with pytest.raises(ValueError):
            generate_playfield(_height, _width)

    @pytest.mark.parametrize('_height,_width', [[1, 2], [2, 1], [3, 4], [4, 3]])
    def test_correct_height_and_width(self, _height, _width):
        """Test the height and width of a generated playfield is correct."""
        _playfield = generate_playfield(_height, _width)
        assert len(_playfield) == _height
        for _row in _playfield:
            assert len(_row) == _width

# Todo: Add tests for other playing field related functions
