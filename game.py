from typing import Tuple

import pygame

from board import Board
from button import Button
import colors
import screen

# required initialization step
pygame.init()


SPEED_UP = -4
SCORE_BETWEEN_SPEED_UPS = 5

class Game(screen.Screen):
    """Runs the game of Tetris"""
    def __init__(self, window: pygame.Surface) -> None:
        super().__init__(window)
        height, width = window.get_height(), window.get_width()
        self.board = Board((int(width / 5), int(height / 10)), (20, 10), 32)
        self.quit_button = Button('Quit', pygame.Rect(0, 9 * height / 10, width / 3, height / 10), colors.BACK_COLOR)
        self.resign_button = Button('Resign', pygame.Rect(2 * width / 3, 9 * height / 10, width / 3, height / 10),
                                    colors.BACK_COLOR)
        self.speed = Board.NORMAL_SPEED
        self.board.new_falling_block()
        self.next_score_milestone = SCORE_BETWEEN_SPEED_UPS

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
            self.events.append(screen.END_SCREEN)
        self.board.update(self.speed)
        self.speed = Board.NORMAL_SPEED
        if self.board.main_block is None:
            self.board.new_falling_block()
        if self.get_score() == self.next_score_milestone:
            self.events.append(SPEED_UP)
            self.next_score_milestone += SCORE_BETWEEN_SPEED_UPS
