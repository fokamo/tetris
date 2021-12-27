"""board.py - for a Board class

For external use:
- Board class for representing a Tetris board
"""

from typing import Union, Tuple

import pygame

from block import Block, random_block, make_shadow_copy
import colors
from square import Square

# required initialization step
pygame.init()

class Board:
    """A Tetris board

    For external use:
    - .NORMAL_SPEED, .FAST_SPEED, .MAX_SPEED for falling-speed constants
    - .draw() to draw the whole board
    - .left(), .right(), and .rotate(clockwise: bool) to move the main block
    - .get_new_falling_block() to generate a new block at the top
    - .update() to handle one frame's worth of logic
    """

    NORMAL_SPEED = 1
    FAST_SPEED = 2
    MAX_SPEED = 0

    def __init__(self, visible_top_left: Tuple[int, int], dimensions: Tuple[int, int], square_size: int) -> None:
        # (rows, cols) 1-indexed
        self.dimensions = dimensions
        self.square_size = square_size

        # components of board

        self.visible_top_left = (visible_top_left[0], visible_top_left[1])
        # top buffer area which pieces spawn into
        self.above_area = pygame.Rect(visible_top_left[0], visible_top_left[1] - 2 * square_size,
                                      dimensions[1] * square_size, 2 * square_size).inflate(Block.PIECE_OUTER_BORDER,
                                                                                            Block.PIECE_OUTER_BORDER)
        # board which pieces fall through
        self.play_area = pygame.Rect(visible_top_left, (square_size * dimensions[1], square_size * dimensions[0]))
        self.bordered_play_area = self.play_area.inflate(Block.PIECE_OUTER_BORDER, Block.PIECE_OUTER_BORDER)

        # initial state
        self.blocks = []
        self.score = 0
        self.dead = False
        self.main_block = None

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, self.above_area)
        pygame.draw.rect(screen, colors.BOARD_COLOR, self.bordered_play_area)

        for bl in self.blocks:
            bl.draw(screen)
        self._draw_main_shadow(screen)

    def _draw_main_shadow(self, screen: pygame.Surface) -> None:
        if self.main_block:
            shadow = make_shadow_copy(self.main_block)
            # remove main block so the shadow doesn't "bump" into it
            self.blocks.remove(self.main_block)

            while self._can_fall(shadow):
                shadow.down()
            shadow.draw(screen)
            self.blocks.append(self.main_block)

    def left(self) -> None:
        self.main_block.left()
        if not self._is_legal(self.main_block):
            self.main_block.right()

    def right(self) -> None:
        self.main_block.right()
        if not self._is_legal(self.main_block):
            self.main_block.left()

    def rotate(self, clockwise: bool) -> None:
        self.main_block.rotate(clockwise)
        if not self._is_legal(self.main_block):
            self.main_block.rotate(not clockwise)

    def get_new_falling_block(self) -> None:
        self.main_block = random_block(self.dimensions[1], self.visible_top_left, self.square_size)
        self.blocks.append(self.main_block)

    def _is_legal(self, item: Union[Block, Square], ignore: Block = None) -> bool:
        if isinstance(item, Block):
            # if all squares in a Block are legal, it's legal
            return all([self._is_legal(sq, item) for sq in item.squares])
        elif isinstance(item, Square):
            # if within all boundaries, and no non-ignored Blocks overlap, then the position is legal
            return item.row() <= self.dimensions[0] and 1 <= item.col() <= self.dimensions[1] and \
                   not any([bl is not ignore and bl.has_square_at(item) for bl in self.blocks])
        else:
            raise TypeError('Object must be a block or square')

    def _can_fall(self, bl: Block) -> bool:
        """Check if a Block can legally fall one unit"""

        bl.down()
        can_fall_flag = self._is_legal(bl)
        bl.up()
        return can_fall_flag

    def _remove_lines(self) -> None:
        """Remove all lines which are completed"""

        # convert 1-indexed pos to 0-indexed for 2D array checking
        occupied = set([(sq.row() - 1, sq.col() - 1) for bl in self.blocks for sq in bl.squares])
        # True for unoccupied cells
        cells = [[(row, col) not in occupied for col in range(self.dimensions[1])] for row in range(self.dimensions[0])]

        for i in range(len(cells)):
            if not any(cells[i]):
                self._remove_line(i + 1)

    def _remove_line(self, row: int) -> None:
        """Remove line & cut pieces"""

        new_blocks = []
        for bl in self.blocks:
            pieces = bl.remove_row(row)
            # if the block was not cut up, just add its original
            if pieces and len(pieces[0].squares) == len(bl.squares):
                new_blocks.append(bl)
            # otherwise add its pieces
            else:
                new_blocks.extend(pieces)
        self.blocks = new_blocks
        self.score += 1

    def update(self, speed: int) -> None:
        # first, all blocks that can, fall
        falls = self.dimensions[0] if speed == Board.MAX_SPEED else speed
        for bl in self.blocks:
            for _ in range(falls):
                if self._can_fall(bl):
                    bl.down()

        # remove any completed lines; if main block was in them get rid of it
        self._remove_lines()
        if self.main_block not in self.blocks:
            self.main_block = None

        # if the main block can't move, check if we've lost and get rid of it
        if self.main_block is not None and not self._can_fall(self.main_block):
            self.dead = min([sq.row() for sq in self.main_block.squares]) <= 0
            self.main_block = None
