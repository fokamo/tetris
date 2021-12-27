"""button.py - for a Button class

For external use:
- Button class for representing a clickable button
"""

import pygame
import fonts
from text import Text

# required initialization step
pygame.init()

class Button(pygame.Rect):
    """A class to represent a button. Subclass of pygame.Rect.

    For external use:
    - is_clicked(mouse_x: int, mouse_y: int) -> bool to check if a given mouseclick-point is on the Button
    - .draw(screen: pygame.Surface) to draw the button
    """

    def __init__(self, label: str, area: pygame.Rect, color: pygame.Color) -> None:
        super().__init__(area)

        # make a text-surface to be blitted later
        self._text = Text(label, fonts.BUTTON_FONT, self, color)
        self._color = color

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if a given mouse click is on the Button.
        mouse_x -- the x coordinate of the mouseclick
        mouse_y -- the y coordinate of the mouseclick
        Returns a bool -- True if the click is on the Button, False if not
        """

        return super().collidepoint(mouse_x, mouse_y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the Button onto a given Surface."""

        # draw rectangle then text on top
        pygame.draw.rect(screen, self._color, self)
        self._text.draw(screen)
