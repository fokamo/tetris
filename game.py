"""game.py - for a game screen class

For external use:
- Game class for a game screen
"""

from typing import Tuple

import pygame

from board import Board
from button import Button
import colors
import screen

# required initialization step
pygame.init()

class Game(screen.Screen):
    """A prepackaged Tetris-game screen. Subclass of Screen

    For external use:
    - .SCORE_BETWEEN_SPEED_UPS for how long to wait before speeding up the game clock
    - .get_score() -> int to get the current board's score
    """

    SCORE_BETWEEN_SPEED_UPS = 3

    def __init__(self, window: pygame.Surface) -> None:
        super().__init__(window)

        height, width = window.get_height(), window.get_width()
        # elements on screen
        self.board = Board((int(width / 5), int(height / 10)), (20, 10), 32)
        self.board.get_new_falling_block()
        self.quit_button = Button('Quit', pygame.Rect(0, 9 * height / 10, width / 3, height / 10),
                                  colors.BACKWARD_COLOR)
        self.resign_button = Button('Resign', pygame.Rect(2 * width / 3, 9 * height / 10, width / 3, height / 10),
                                    colors.BACKWARD_COLOR)

        # current state
        self.speed = Board.NORMAL_SPEED
        self.next_score_milestone = Game.SCORE_BETWEEN_SPEED_UPS

    def handle_click(self, mouse_pos: Tuple[int, int]) -> None:
        if self.quit_button.is_clicked(mouse_pos[0], mouse_pos[1]):
            self.events.append(screen.EXIT_GAME)
        elif self.resign_button.is_clicked(mouse_pos[0], mouse_pos[1]):
            self.events.append(screen.END_SCREEN)

    def handle_key(self, key: int) -> None:
        if key in (pygame.K_UP, pygame.K_x, pygame.K_1, pygame.K_5, pygame.K_9):
            self.board.rotate(True)
        elif key in (pygame.K_RCTRL, pygame.K_LCTRL, pygame.K_z, pygame.K_3, pygame.K_7):
            self.board.rotate(False)
        elif key == pygame.K_LEFT:
            self.board.left()
        elif key == pygame.K_RIGHT:
            self.board.right()
        elif key == pygame.K_DOWN:
            self.speed = Board.FAST_SPEED
        elif key in (pygame.K_SPACE, pygame.K_8):
            self.speed = Board.MAX_SPEED

    def draw(self) -> None:
        self.board.draw(self.window)
        self.quit_button.draw(self.window)
        self.resign_button.draw(self.window)

    def get_score(self) -> int:
        return self.board.score

    def update(self) -> None:
        if self.board.dead:
            self.events.extend([screen.END_SCREEN, screen.RESET_SPEED])
        else:
            self.board.update(self.speed)
            # reset speed so next update isn't extra fast
            self.speed = Board.NORMAL_SPEED
            if self.board.main_block is None:
                self.board.get_new_falling_block()
            if self.get_score() == self.next_score_milestone:
                self.events.append(screen.SPEED_UP)
                self.next_score_milestone += Game.SCORE_BETWEEN_SPEED_UPS
