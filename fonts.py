"""fonts.py - a central file of fonts

For external use:
- .TITLE_FONT, .SUBTITLE_FONT (both inkfree, subtitle is smaller and italicized)
- .BUTTON_FONT (calibri)
"""

import pygame

# required initialization step
pygame.init()

TITLE_FONT = pygame.font.SysFont('inkfree', 60)
SUBTITLE_FONT = pygame.font.SysFont('inkfree', 20, False, True)
BUTTON_FONT = pygame.font.SysFont('calibri', 35)
