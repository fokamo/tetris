import point
import pygame

from typing import Tuple

# required initialization step
pygame.init()

class Square(point.Point):
    """A square in a game grid. Subclass of Point

    For external use:
    - .size and .rect for information about the on-screen square
    - .board_top.left for where the top left of the grid is
    """

    def __init__(self, pos: Tuple[float, float], size: int, board_left_top: Tuple[int, int]) -> None:
        super().__init__(pos)
        self.board_left_top = board_left_top
        self.size = size
        self.rect = pygame.Rect(0, 0, size, size)
        self._set_rect()

    def _set_rect(self):
        self.rect.left = self.board_left_top[0] + (self.size * (self.col() - 1))
        self.rect.top = self.board_left_top[1] + (self.size * (self.row() - 1))

    def _move(self, row_move, col_move) -> None:
        super()._move(row_move, col_move)
        self.rect.move_ip(col_move * self.size, row_move * self.size)

    def teleport(self, new_pos: Tuple[float, float]) -> None:
        super().teleport(new_pos)
        self._set_rect()
