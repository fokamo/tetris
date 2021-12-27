"""end.py - for an ending screen class

For external use:
- End class for an ending screen
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

class End(screen.Screen):
    """A prepackaged ending celebration screen. Subclass of Screen"""

    def __init__(self, window: pygame.Surface, score: int) -> None:
        super().__init__(window)
        width, height = window.get_width(), window.get_height()
        # elements on screen
        self.label_line = get_text_by_center('Score:', fonts.SUBTITLE_FONT, (width / 2, height / 5),
                                             colors.BACKGROUND_COLOR)
        self.score_line = get_text_by_center(str(score), fonts.TITLE_FONT, (width / 2, height / 2),
                                             colors.BACKGROUND_COLOR)
        self.quit_button = Button('Quit', pygame.Rect(0, 9 * height / 10, width / 3, height / 10), colors.BACKWARD_COLOR)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        if self.quit_button.is_clicked(mouse_pos[0], mouse_pos[1]):
            self.events.append(screen.EXIT_GAME)

    def draw(self):
        self.label_line.draw(self.window)
        self.score_line.draw(self.window)
        self.quit_button.draw(self.window)
