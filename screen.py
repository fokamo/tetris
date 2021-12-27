"""screen.py - for a Screen class

For external use:
- Screen class for representing a game screen
- EXIT_GAME, GAME_SCREEN, END_SCREEN constants and CHANGE_SCREEN array for state representation
- SPEED_UP, RESET_SPEED constants for speed events
"""

from typing import List, Tuple
import pygame

import colors


# required initialization step
pygame.init()

# constants for use elsewhere
EXIT_GAME = -1
GAME_SCREEN = -2
END_SCREEN = -3
SPEED_UP = -4
RESET_SPEED = -5
CHANGE_SCREEN = [GAME_SCREEN, END_SCREEN]

class Screen:
    """A generic game screen

    For external use:
    - .handle_click(mouse_pos) and .handle_key(key) to handle outside events
    - .get_events() to get backlogged events
    - .draw() to draw self
    - .update() to handle any necessary updates
    """

    def __init__(self, window: pygame.Surface) -> None:
        self.events = []
        self.window = window

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        """Handle a mouseclick"""
        pass

    def handle_key(self, key: int) -> None:
        """Handle a keypress"""
        pass

    def get_events(self) -> List[int]:
        """Get backlogged events, consuming all"""
        old_events = self.events
        self.events = []
        return old_events

    def draw(self) -> None:
        """Draw current state"""
        self.window.fill(colors.BACKGROUND_COLOR)

    def update(self) -> None:
        """Handle any internal updates"""
        pass
