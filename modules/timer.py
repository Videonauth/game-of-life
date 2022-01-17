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

    def timer_increment(self):
        """Return the timer increment."""
        return self._current_time - self._last_time

    def poll(self, frame_limit: float):
        """Wait if to fast, skip (return True) if to slow."""
        self._current_time = time.time()
        if self.timer_increment() <= frame_limit:
            _wait = frame_limit - self.timer_increment()
            self._last_frame_time = self.timer_increment() + _wait
            time.sleep(_wait)
            self._last_time = time.time()
            return False
        else:
            self._last_frame_time = self.timer_increment()
            self._last_time = time.time()
            return True

    def last_frame_time(self):
        """Return last frame time."""
        return self._last_frame_time
