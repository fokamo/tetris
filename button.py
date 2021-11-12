"""button.py: for a Button class"""

import pygame
import text, fonts

# required initialization step
pygame.init()


class Button(pygame.Rect):
    """A class to represent a button. Subclass of pygame.Rect.
    Attributes:
    left, top, width, height -- from Rect
    _text -- Button's label
    _color -- background color of the Button
    Methods:
    is_clicked -- checks if a given mouseclick-point is on the Button
    draw -- draws the Button on a Surface
    In all cases the origin (0, 0) is the top left corner
    """

    def __init__(self, label: str, area: pygame.Rect, color: pygame.Color
                 ) -> None:
        """Initialize a Button.
        text -- label on Button
        area -- Rect where the Button should go
        color -- background color of the Button
        """

        super().__init__(area)

        # make a text-surface to be blitted later
        self._text = text.Text(label, fonts.BUTTON_FONT, self, color)
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