#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - test_suite
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 11.01.22 - 22:55
# Purpose: -
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""Testsuite for generate_playfield."""

from modules.playfield import generate_playfield, generate_seeded_playfield, serialize_playfield

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


class TestSeededPlayingFieldFactory:
    """Testsuite for generate_seeded_playfield factory."""

    @pytest.mark.parametrize('_height,_width', [[0, 1], [1, 0], [-1, 1], [1, -2], [0, 0]])
    def test_non_positive_numbers_yield_exceptions(self, _height, _width):
        """Non-positive arguments yield ValueError."""
        with pytest.raises(ValueError):
            generate_seeded_playfield(_height, _width, 0)

    def test_exception_raised_if_both_dimensions_are_one(self):
        """Value error yielded if both dimensions have magnitude one."""
        _height = 1
        _width = 1
        with pytest.raises(ValueError):
            generate_seeded_playfield(_height, _width, 0)

    @pytest.mark.parametrize('_height,_width', [[1, 2], [2, 1], [3, 4], [4, 3]])
    def test_correct_height_and_width(self, _height, _width):
        """Test the height and width of a generated playfield is correct."""
        _playfield = generate_seeded_playfield(_height, _width, 0)
        assert len(_playfield) == _height
        for _row in _playfield:
            assert len(_row) == _width

    @pytest.mark.parametrize('_seed', [-1, -2, -3])
    def test_seed_value_less_than_zero_yields_value_error(self, _seed):
        """Test the seed value is at least zero."""
        _height = 2
        _width = 2
        _playfield_size = _height * _width
        with pytest.raises(ValueError) as ex:
            generate_seeded_playfield(_height, _width, _seed)
        assert str(ex.value) == f'_number_of_seeded_cells too small: must be in the range [0, {_playfield_size}]'

    def test_seed_value_zero_yields_playfield_with_no_cells_mutated(self):
        """Test a seed value of zero yields a playfield with no mutated cells."""
        _height = 2
        _width = 2
        _seed = 0
        _playfield = generate_seeded_playfield(_height, _width, _seed)
        expected = 0
        actual = sum([1 for _row in _playfield for _cell in _row if _cell == 1])
        assert actual == expected

    @pytest.mark.parametrize('_seed', [5, 6, 7])
    def test_seed_value_greater_than_playfield_size_yields_value_error(self, _seed):
        """Test the seed value is at least zero."""
        _height = 2
        _width = 2
        _playfield_size = _height * _width
        with pytest.raises(ValueError) as ex:
            generate_seeded_playfield(_height, _width, _seed)
        assert str(ex.value) == f'_number_of_seeded_cells too large: must be in the range [0, {_playfield_size}]'

    def test_seed_value_of_size_playfield_size_yields_correct_number_of_mutated_cells(self):
        """Test a seed value of playfield size yields a playfield with the correct number of mutated cells.

        seed size == height * width should yield correct number of mutated cells.
        """
        _height = 2
        _width = 2
        _playfield_size = _height * _width
        _seed = _playfield_size
        _playfield = generate_seeded_playfield(_height, _width, _seed)
        expected = _playfield_size
        actual = sum([1 for _row in _playfield for _cell in _row if _cell == 1])
        assert actual == expected

    @pytest.mark.parametrize('_seed', [*range(0, 26)])
    def test_seed_value_size_yields_correct_number_of_mutated_cells(self, _seed):
        """Test a seed value yields a playfield with the correct number of mutated cells."""
        _height = 5
        _width = 5
        _playfield = generate_seeded_playfield(_height, _width, _seed)
        expected = _seed
        actual = sum([1 for _row in _playfield for _cell in _row if _cell == 1])
        assert actual == expected


class TestPlayingSerialization:
    """Test-suite for serialize_playfield."""

    def test_non_list_input_yields_value_error(self):
        """Test the input must be a list."""
        with pytest.raises(ValueError) as ex:
            serialize_playfield(0)
        assert str(ex.value) == '_playfield is not a list'

    def test_if_playfield_is_not_list_of_lists_serializer_yields_value_error(self):
        """Test the input must be a list of lists."""
        with pytest.raises(ValueError) as ex:
            serialize_playfield([0])
        assert str(ex.value) == '_playfield is not a list of lists'

    @pytest.mark.parametrize(
        '_playfield,expected_output',
        [
            ([[0, 0]], '0  0'),
            ([[0, 0, 1]], '0  0  1'),
            ([[0, 1, 0]], '0  1  0'),
            ([[0, 1, 0], [1, 0, 0]], '0  1  0\n1  0  0'),
            ([[1, 0, 0], [1, 0, 0]], '1  0  0\n1  0  0'),
            ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], '1  0  0\n0  1  0\n0  0  1'),
        ])
    def test_various_configurations_yield_correct_output(self, _playfield, expected_output):
        """Test the serialized playfields yield expected output."""
        actual = serialize_playfield(_playfield)
        assert actual == expected_output
