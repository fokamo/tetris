"""board.py - for a Board class

For external use:
- Board class for representing a Tetris board
"""

from typing import Union, Tuple

import pygame

from block import Block, random_block, make_shadow_copy
import colors
from point import Point

class Board:
    """A Tetris board

    For external use:
    - .NORMAL_SPEED, .FAST_SPEED, .MAX_SPEED for falling-speed constants
    - .PIECE_OUTER_BORDER and .PIECE_INNER_BORDER for piece border thickness constants
    - .draw() to draw the whole board
    - .left(), .right(), and .rotate(clockwise: bool) to move the main block
    - .new_falling_block() to generate a new block at the top
    - .is_inbounds(item), has_overlap(item, ignore), can_fall(block) to check for those things for any Block or Square
    - .remove_lines() and .remove_line(row: int) to remove either all completed lines or just one
    - .update() to handle one frame's worth of logic
    """

    NORMAL_SPEED = 1
    FAST_SPEED = 2
    MAX_SPEED = 0

    PIECE_OUTER_BORDER = 3
    PIECE_INNER_BORDER = 1

    def __init__(self, visible_top_left: Tuple[int, int], dimensions: Tuple[int, int], square_size: int) -> None:
        # (rows, cols) 1-indexed
        self.dimensions = dimensions

        visible_top_left = (visible_top_left[0], visible_top_left[1])
        self.above_area = pygame.Rect(visible_top_left[0], visible_top_left[1] - 2 * square_size,
                                      dimensions[1] * square_size, 2 * square_size)
        self.play_area = pygame.Rect(visible_top_left, (square_size * dimensions[1], square_size * dimensions[0]))

        # initial state
        self.blocks = []
        self.score = 0
        self.dead = False
        self.main_block = None

    def draw(self, screen: pygame.Surface) -> None:
        # margin given to color over the borders of pieces
        # buffer top area which pieces spawn into
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, self.above_area.inflate(Board.PIECE_OUTER_BORDER,
                                                                                  Board.PIECE_OUTER_BORDER))
        # board which pieces fall through
        pygame.draw.rect(screen, colors.BOARD_COLOR, self.play_area.inflate(Board.PIECE_OUTER_BORDER,
                                                                            Board.PIECE_OUTER_BORDER))

        square_size = (int(self.play_area.width / self.dimensions[1]), int(self.play_area.height / self.dimensions[0]))
        self._draw_main_shadow(screen, square_size)

        for bl in self.blocks:
            self._draw_block(screen, bl, square_size)

    def _draw_main_shadow(self, screen: pygame.Surface, square_size: Tuple[int, int]) -> None:
        if self.main_block:
            shadow = make_shadow_copy(self.main_block)
            # remove main block so the shadow doesn't "bump" into it
            self.blocks.remove(self.main_block)
            while self.can_fall(shadow):
                shadow.down()
            self._draw_block(screen, shadow, square_size)
            self.blocks.append(self.main_block)

    def _draw_block(self, screen: pygame.Surface, bl: Block, square_size: Tuple[int, int]) -> None:
        for sq in bl.squares:
            # (left, top) coordinate of current square
            top_left = (self.play_area.left + (square_size[0] * (sq.pos[1] - 1)),
                        self.play_area.top + (square_size[1] * (sq.pos[0] - 1)))
            # draw square itself
            pygame.draw.rect(screen, bl.color,
                             pygame.Rect(top_left[0], top_left[1], square_size[0], square_size[1]))

            for is_x in range(2):
                for i in range(2):
                    adj = Point((sq.row() + (not is_x) * ((i * 2) - 1), sq.col() + is_x * ((i * 2) - 1)))
                    border_width = Board.PIECE_INNER_BORDER if bl.has_square_at(adj) else Board.PIECE_OUTER_BORDER

                    # starts at left unless 2nd x (i.e. left), starts at top unless 2nd y (i.e. bottom)
                    border_start = (top_left[0] + square_size[0] if i and is_x else top_left[0],
                                    top_left[1] + square_size[1] if i and not is_x else top_left[1])
                    # ends at right unless 1st x (i.e. right), ends at bottom unless 1st y (i.e. top)
                    border_end = (top_left[0] + square_size[0] if i or not is_x else top_left[0],
                                  top_left[1] + square_size[1] if i or is_x else top_left[1])
                    pygame.draw.line(screen, colors.BLACK, border_start, border_end, border_width)

    def left(self) -> None:
        self.main_block.left()
        if self.has_overlap(self.main_block) or not self.is_inbounds(self.main_block):
            self.main_block.right()

    def right(self) -> None:
        self.main_block.right()
        if self.has_overlap(self.main_block) or not self.is_inbounds(self.main_block):
            self.main_block.left()

    def rotate(self, clockwise: bool) -> None:
        self.main_block.rotate(clockwise)
        if not self.is_inbounds(self.main_block):
            self.main_block.rotate(not clockwise)

    def new_falling_block(self) -> None:
        self.main_block = random_block(self.dimensions[1])
        self.blocks.append(self.main_block)

    def is_inbounds(self, item: Union[Block, Point]) -> bool:
        if isinstance(item, Block):
            # if any squares in a Block are not inbounds, then it is out of bounds
            return not any([not self.is_inbounds(sq) for sq in item.squares])
        elif isinstance(item, Point):
            # check for not exceeding left, right, or bottom bounds
            return item.row() <= self.dimensions[0] and 1 <= item.col() <= self.dimensions[1]
        else:
            raise TypeError('Object must be a block or point')

    def has_overlap(self, item: Union[Block, Point], ignore: Block = None) -> bool:
        if isinstance(item, Block):
            # if any squares in a Block overlap, then it has an overlap
            return any([self.has_overlap(sq, item) for sq in item.squares])
        elif isinstance(item, Point):
            # check for overlap with all non-ignored Blocks
            return any([bl is not ignore and bl.has_square_at(item) for bl in self.blocks])
        else:
            raise TypeError('Object must be a block or point')

    def can_fall(self, bl: Block) -> bool:
        bl.down()
        can_fall_flag = self.is_inbounds(bl) and not self.has_overlap(bl)
        bl.up()
        return can_fall_flag

    def remove_lines(self) -> None:
        """Remove all lines which are completed"""

        occupied = set([(sq.row() - 1, sq.col() - 1) for bl in self.blocks for sq in bl.squares])
        # True for unoccupied cells
        cells = [[(row, col) not in occupied for col in range(self.dimensions[1])] for row in range(self.dimensions[0])]

        for i in range(len(cells)):
            if not any(cells[i]):
                self.remove_line(i + 1)

    def remove_line(self, row: int) -> None:
        """Remove line & cut pieces"""
        print(row)

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
                if self.can_fall(bl):
                    bl.down()

        # remove any completed lines; if main block was in them get rid of it
        self.remove_lines()
        if self.main_block not in self.blocks:
            self.main_block = None

        # if the main block can't move, check if we've lost and get rid of it
        if self.main_block is not None and not self.can_fall(self.main_block):
            self.dead = min([sq.row() for sq in self.main_block.squares]) <= 0
            self.main_block = None
