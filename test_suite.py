#!/usr/bin/env pytest

import pytest

from game_of_life import generate_playingfield


class TestPlayingFieldFactory:
    @pytest.mark.parametrize('height,width', [[0, 1], [1, 0], [-1, 1], [1, -2], [0, 0]])
    def test_non_positive_numbers_yield_exceptions(self, height, width):
        with pytest.raises(ValueError):
            generate_playingfield(height, width)

    def test_exception_raised_if_both_dimensions_are_one(self):
        height = 1
        width = 1
        with pytest.raises(ValueError):
            generate_playingfield(height, width)

    @pytest.mark.parametrize('height,width', [[1, 2], [2, 1], [3, 4], [4, 3]])
    def test_correct_height_and_width(self, height, width):
        playingfield = generate_playingfield(height, width)
        assert len(playingfield) == height
        for row in playingfield:
            assert len(row) == width

