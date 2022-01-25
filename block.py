"""block.py - for a Block class

For external use:
- Block class for representing a Tetris block
- make_shadow_copy(original: Block) function for generating a shadow-colored replica of a block
- find_connected_groups(points: List[Point]) function for doing that to lists of Points
- random_block(columns: int) function for generating a random standard Tetris piece
"""

from __future__ import annotations

import random
from typing import List, Set, Callable, Tuple

import pygame

import colors
from square import Square
from point import Point, are_adj_points

# required initialization step
pygame.init()

class Block:
    """A Tetris block

    For external use:
    - .PIECE_OUTER_BORDER and .PIECE_INNER_BORDER for piece border thickness constants
    - .draw(screen: pygame.Surface) to draw the Block
    - .has_square_at(pt: Point) -> bool to check just that
    - .down(), .up(), .left(), and .right() to move the Block 1 unit in such direction
    - .rotate(clockwise: bool) to rotate the Block around its center
    - .remove_row(row: int) -> List[Block] to delete a given row of squares and return the pieces
    - .__eq__(other), .__ne__(other), .__hash__(), and .__str__() overridden
    """

    PIECE_OUTER_BORDER = 3
    PIECE_INNER_BORDER = 1

    def __init__(self, color: pygame.Color, pos: List[Tuple[float, float]], center: Tuple[float, float],
                 board_left_top: Tuple[int, int], square_size: int) -> None:
        self.color = color

        # information for Block's squares
        self.squares = [Square(p, square_size, board_left_top) for p in pos]
        self.center = Point(center)

        # for easy looping over later - must move each square & center point in tandem
        self._to_move = list(self.squares)
        self._to_move.append(self.center)

    def draw(self, screen: pygame.Surface) -> None:
        size = self.squares[0].size
        for sq in self.squares:
            pygame.draw.rect(screen, self.color, sq.rect)
            left_top = (sq.rect.left, sq.rect.top)

            for is_x in range(2):
                for i in range(2):
                    adj = Point((sq.row() + (not is_x) * ((i * 2) - 1), sq.col() + is_x * ((i * 2) - 1)))
                    border_width = Block.PIECE_INNER_BORDER if self.has_square_at(adj) else Block.PIECE_OUTER_BORDER

                    # starts at left unless 2nd x (i.e. left), starts at top unless 2nd y (i.e. bottom)
                    border_start = (left_top[0] + size if (i and is_x) else left_top[0],
                                    left_top[1] + size if (i and not is_x) else left_top[1])
                    # ends at right unless 1st x (i.e. right), ends at bottom unless 1st y (i.e. top)
                    border_end = (left_top[0] + size if (i or not is_x) else left_top[0],
                                  left_top[1] + size if (i or is_x) else left_top[1])
                    pygame.draw.line(screen, colors.BLACK, border_start, border_end, border_width)

    def has_square_at(self, pt: Point) -> bool:
        return pt.pos in [sq.pos for sq in self.squares]

    # aliases for _move() for outside use
    def down(self) -> None:
        self._move(Point.down)

    def up(self) -> None:
        self._move(Point.up)

    def left(self) -> None:
        self._move(Point.left)

    def right(self) -> None:
        self._move(Point.right)

    def _move(self, direction: Callable) -> None:
        for moving in self._to_move:
            direction(moving)

    def rotate(self, clockwise: bool) -> None:
        for sq in self.squares:
            row_dist = sq.row() - self.center.row()
            col_dist = sq.col() - self.center.col()

            # swap y and x distances
            if clockwise:
                new_x = self.center.col() - row_dist
                new_y = self.center.row() + col_dist
            else:
                new_x = self.center.col() + row_dist
                new_y = self.center.row() - col_dist

            sq.teleport((new_y, new_x))

    def remove_row(self, row: int) -> List[Block]:
        return [Block(colors.BROKEN_PIECE_COLOR, [sq.pos for sq in group], group[0].pos,
                      self.squares[0].board_left_top, self.squares[0].size)
                for group in find_connected_groups([sq for sq in self.squares if sq.pos[0] != row])]

    # overriding comparison methods
    def __eq__(self, other) -> bool:
        return isinstance(other, Block) and self.__key() == other.__key()

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __key(self) -> Tuple[Set[Point], Tuple[float, float, float]]:
        return set(self._to_move), self.color.cmy

    def __hash__(self) -> int:
        return hash(self.__key())

    # for debugging, mostly
    def __str__(self) -> str:
        return '[' + ', '.join([sq.__str__() for sq in self.squares]) + ']'


def make_shadow_copy(original: Block) -> Block:
    """Create a shadow-colored copy of a Block in the same position"""

    return Block(colors.SHADOW_COLOR, [sq.pos for sq in original.squares], original.center.pos,
                 original.squares[0].board_left_top, original.squares[0].size)

def find_connected_groups(points: List[Point]) -> List[List[Point]]:
    """Find connected groups of Points"""

    # create a graph of points: adj points, but only map if there are adj sqs
    adj_graph = {pt: adjs for pt in points if (adjs := [adj for adj in points if are_adj_points(pt, adj)])}
    # initialize each point to own group
    groups = [[pt] for pt in points]
    # graph of points to which group they're in
    points_to_groups = {points[i]: i for i in range(len(points))}

    # while there are points with unresolved adjacencies
    while adj_graph:
        # grab some point to merge with its adjacencies
        cur_point = next(iter(adj_graph.keys()))
        acceptor_group = points_to_groups[cur_point]
        adjs = adj_graph[cur_point]

        # while there are adjacencies left to merge
        while adjs:
            # for all the points in this adjacent point's group
            adj_point_group = points_to_groups[next(iter(adjs))]

            for adj_point in groups[adj_point_group]:
                # add to original point's group
                groups[acceptor_group].append(adj_point)
                points_to_groups[adj_point] = acceptor_group

                # the merged point has had its adjacencies effectively resolved
                if adj_point in adj_graph:
                    del adj_graph[adj_point]
                # remove from points-to-merge if applicable
                if adj_point in adjs:
                    adjs.remove(adj_point)
            # this group is used up
            groups[adj_point_group] = []
        del adj_graph[cur_point]
    return [group for group in groups if group]

# factories for standard Tetris pieces
def _make_I_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    return Block(colors.I_COLOR, [(O_bottom_left[0], O_bottom_left[1] - i + 1) for i in range(4)],
                 (O_bottom_left[0] + 0.5, O_bottom_left[1] - 0.5), board_left_top, square_size)

def _make_O_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    return Block(colors.O_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j) for i in range(2) for j in range(2)],
                 (O_bottom_left[0] - 0.5, O_bottom_left[0] - 0.5), board_left_top, square_size)

def _make_T_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1]))
    return Block(colors.T_COLOR, straight, O_bottom_left, board_left_top, square_size)

def _make_S_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    return Block(colors.S_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j + 1 - i)
                                  for i in range(2) for j in range(2)], O_bottom_left, board_left_top, square_size)

def _make_Z_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    return Block(colors.Z_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j + i)
                                  for i in range(2) for j in range(2)], O_bottom_left, board_left_top, square_size)

def _make_J_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1] + 1))
    return Block(colors.J_COLOR, straight, O_bottom_left, board_left_top, square_size)

def _make_L_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1] - 1))
    return Block(colors.L_COLOR, straight, O_bottom_left, board_left_top, square_size)

def random_block(O_bottom_left: Tuple[int, int], board_left_top: Tuple[int, int], square_size: int) -> Block:
    """Create a random standard Tetris piece"""
    return random.choice((_make_I_block, _make_O_block, _make_T_block, _make_S_block,
                          _make_Z_block, _make_J_block, _make_L_block))(O_bottom_left, board_left_top, square_size)
