#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# game-of-life - input
# ---------------------------------------------------------------------------
# Author: Videonauth <videonauth@googlemail.com>
# License: MIT (see LICENSE file)
# Date: 15.01.22 - 20:33
# Purpose: -
# Written for: Python 3.9.5
# ---------------------------------------------------------------------------
"""Input Handler Class."""
from collections import namedtuple

import pygame


HandlerPoll = namedtuple('HandlerPoll', ['x', 'y', 'event_x', 'event_y', 'event_button', 'event_key'])


class InputHandler:
    """Handler Class."""

    def __init__(self):
        """Initialize the handler."""
        if not pygame.get_init():
            pygame.init()
        self._running = True
        self._key_pressed = False
        self._button_pressed = False
        self._locked = False

    def lock(self):
        """Set internal lock."""
        self._locked = True
        return

    def unlock(self):
        """Unset internal lock."""
        self._locked = False
        return

    def locked(self):
        """Return the internal boolean value."""
        return self._locked

    def running(self):
        """Return the internal boolean value."""
        return self._running

    def button_pressed(self):
        """Return the internal boolean value."""
        return self._button_pressed

    def key_pressed(self):
        """Return the internal boolean value."""
        return self._key_pressed

    def poll(self):
        """Poll for input events."""
        event_x = 0
        event_y = 0
        event_button = 0
        event_key = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # set the _running boolean to false.
                self._running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self._button_pressed:
                event_x, event_y = event.pos
                event_button = event.button
                self._button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self._locked = False
                self._button_pressed = False
            if event.type == pygame.KEYDOWN and not self._key_pressed:
                event_key = event.key
                self._key_pressed = True
            elif event.type == pygame.KEYUP:
                self._locked = False
                self._key_pressed = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        return HandlerPoll(mouse_x, mouse_y, event_x, event_y, event_button, event_key)
