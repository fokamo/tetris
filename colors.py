"""colors.py - a central file of colors

For external use:

- .BACKGROUND_COLOR, .BLACK, .BOARD_COLOR for misc., widely-used colors
- .FORWARD_COLOR, .BACKWARD_COLOR for button colors
- .BROKEN_PIECE_COLOR, .SHADOW_COLOR, .I_/.O_/.T_/.S_/.Z_/.J_/.L_COLOR for Tetris pieces
"""

import pygame

# required initialization step
pygame.init()

# misc. colors
BACKGROUND_COLOR = pygame.Color(38, 228, 235)
BLACK = pygame.Color(0, 0, 0)
BOARD_COLOR = pygame.Color(212, 177, 125)

# button colors
FORWARD_COLOR = pygame.Color(24, 194, 12)
BACKWARD_COLOR = pygame.Color(235, 91, 91)

# piece colors
BROKEN_PIECE_COLOR = pygame.Color(127, 127, 127)
SHADOW_COLOR = pygame.Color(64, 64, 64)
I_COLOR = pygame.Color(0, 255, 255)  # Cyan I
O_COLOR = pygame.Color(255, 255, 0)  # Yellow O
T_COLOR = pygame.Color(128, 0, 128)  # Purple T
S_COLOR = pygame.Color(0, 255, 0)    # Green S
Z_COLOR = pygame.Color(255, 0, 0)    # Red Z
J_COLOR = pygame.Color(0, 0, 255)    # Blue J
L_COLOR = pygame.Color(255, 127, 0)  # Orange L
