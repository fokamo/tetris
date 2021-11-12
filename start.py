"""start.py - for an starting intro screen class

For external use:
- Start class for a starting screen
"""

from typing import Tuple

import pygame

from button import Button
import colors
import fonts
import screen
from text import get_text_by_center

# required initialization step
pygame.init()


class Start(screen.Screen):
    """Starting intro screen. Subclass of Screen"""

    def __init__(self, window: pygame.Surface) -> None:
        super().__init__(window)
        width, height = window.get_width(), window.get_height()
        self.title = get_text_by_center('TETRIS', fonts.TITLE_FONT, (width / 2, height / 4), colors.BACKGROUND_COLOR)
        self.start_button = Button('Start', pygame.Rect(width / 4, 3 * height / 5, width / 2, height / 5),
                                   colors.FORWARD_COLOR)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        if self.start_button.is_clicked(mouse_pos[0], mouse_pos[1]):
            self.events.append(screen.GAME_SCREEN)

    def draw(self):
        self.title.draw(self.window)
        self.start_button.draw(self.window)
