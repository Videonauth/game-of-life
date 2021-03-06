#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - timer
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 16.01.22 - 02:22
# Purpose: -
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------

"""Timer class."""
import time


class Timer:
    """Timer class."""

    def __init__(self):
        """Initialize the timer object."""
        self._last_time = time.time()
        self._current_time = time.time()
        self._last_frame_time = 0.001

    def poll(self, frame_limit: float):
        """Wait if to fast, skip (return True) if to slow."""
        self._current_time = time.time()
        if self._current_time - self._last_time <= frame_limit:
            _wait = frame_limit - (self._current_time - self._last_time)
            self._last_frame_time = (self._current_time - self._last_time) + _wait
            time.sleep(_wait)
            self._last_time = time.time()
            return False
        elif self._current_time - self._last_time > frame_limit:
            self._last_frame_time = (self._current_time - self._last_time)
            self._last_time = time.time()
            return True
        else:
            return False

    def last_frame_time(self):
        """Return last frame time."""
        return self._last_frame_time
