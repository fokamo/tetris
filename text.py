"""text.py: for a Text class
Classes:
Text -- for easy textbox handling
Methods:
paragraphs_to_lines -- convert paragraphs to line-by-line Texts
get_text_by_center -- generate a text box which is centered on the given point
"""

import pygame
import colors

# required initialization step
pygame.init()


class Text:
    """A class to represent a textbox.
    Attributes:
    _text -- Surface with text on it
    _pos -- the (left, top) corner of the textbox
    Methods:
    draw -- draws the Text on a Surface
    """

    def __init__(self, text: str, font: pygame.font.Font,
                 area: pygame.Rect, background_color: pygame.Color,
                 centered=True) -> None:
        """Initialize a Text.
        text -- string to display
        font -- Font the text is to be displayed in
        area -- Rect where the text should go
        background_color -- expected background color for this text
        centered -- whether the text should center itself in its box
                 -- defaults to True
        """

        # create the needed text-surface
        self._text = font.render(text, True, colors.BLACK, background_color)

        if centered:
            # get (top, left) position to center text with
            self._pos = self._center_text(area)
        else:
            # just use top-left corner as usual
            self._pos = (area.left, area.top)

    def _center_text(self, area: pygame.Rect) -> (int, int):
        """Calculate top-left corner to center text within a rectangle.
        text -- text-surface which needs to be centered
        area -- Rect which the text should be centered in
        Returns a tuple with (left, top) for a centered text position
        """

        # temporary text Rect, used to grab width/height for centering text
        temp_rect = self._text.get_rect()
        # center within rectangle, accounting for the text's size itself
        return (area.left + (area.width / 2) - (temp_rect.width / 2),
                area.top + (area.height / 2) - (temp_rect.height / 2)
                )

    def draw(self, screen: pygame.Surface):
        """Draw the text onto a given Surface."""

        screen.blit(self._text, self._pos)


def paragraphs_to_lines(paragraphs: list, font: pygame.font.Font,
                        area: pygame.Rect, background_color: pygame.Color
                        ) -> list:
    """Convert paragraphs to line-by-line Texts.
    paragraphs -- list of paragraphs to convert
    font -- Font the text is to be displayed in
    area -- Rect where the text should go
    background_color -- expected background Color for this text
    Returns a list of Texts, one for each broken-up line of the paragraphs
    """

    # return variable
    lines = []

    # 2D array: first level is list of paragraphs, second level is list of words
    text = [paragraph.split(' ') for paragraph in paragraphs]

    # the first y-value that should be used is just the top of the area
    y = area.top

    for paragraph in text:
        # reset current line
        line_length = 0
        cur_line = []

        for word in paragraph:
            # grab width & height of this word
            word_width = font.render(word, True, colors.BLACK).get_size()[0]

            # if this word would cause an overflow
            if line_length + word_width >= area.width:
                # grab line so far
                final_line = " ".join(cur_line)
                line_height = font.render(final_line, True,
                                          colors.BLACK).get_size()[1]

                # create Text and add to list
                lines.append(Text(final_line, font,
                                  pygame.Rect(area.left, y, area.width,
                                              line_height),
                                  background_color, False))

                # reset back down to next line
                y += line_height + 1
                line_length = 0
                cur_line = []

            # no matter what, now add this word to growing line
            cur_line.append(word)
            line_length += word_width

        # grab leftover words in paragraph
        final_line = " ".join(cur_line)
        line_height = font.render(final_line, True, colors.BLACK).get_size()[1]

        # create Text and add to list
        lines.append(Text(final_line, font,
                          pygame.Rect(area.left, y, area.width, line_height),
                          background_color, False))

        # double-step down for paragraph break
        y += (2 * (line_height + 1))

    return lines


def get_text_by_center(text: str, font: pygame.font.Font, center: (int, int),
                       background_color: pygame.Color) -> Text:
    """Generate a text box which is centered on the given point.
    text -- string to display
    font -- Font the text is to be displayed in
    center -- point the text should be centered at
    background_color -- expected background Color for this text
    Returns a Text with the given text, font, and a centered position
    """

    # grab size of text
    text_width, text_height = font.render(text, True, colors.BLACK).get_size()
    # calculate just-big-enough centered text rectangle
    centered_area = pygame.Rect(center[0] - (text_width / 2),
                                center[1] - (text_height / 2),
                                text_width, text_height)

    return Text(text, font, centered_area, background_color)