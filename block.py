"""block.py - for a Point class

For external use:
- Block class for representing a Tetris block
- make_shadow_copy(original: Block) function for generating a shadow-colored replica of a block
- find_connected_groups(points: List[Point]) function for doing that to lists of Points
- random_block(columns: int) function for generating a random standard Tetris piece
"""


from __future__ import annotations

import random
from typing import List, Set, Callable, Tuple, Dict

import pygame

import colors
from point import Point, are_adj

# required initialization step
pygame.init()


class Block:
    """A Tetris block

    For external use:
    - .has_square_at(p: Point) to check just that
    - .down(), .up(), .left(), and .right() to move the Block 1 unit in such direction
    - .rotate(clockwise: bool) to rotate the Block around its center
    - .remove_row(row: int) to delete a given row of squares and return the pieces
    - .__eq__(other), .__ne__(other), .__hash__(), and .__str__() overridden
    """

    def __init__(self, color: pygame.Color, pos: List[Tuple[float, float]], center: Tuple[float, float]) -> None:
        self.color = color
        self.squares = [Point(p) for p in pos]
        self.center = Point(center)

        # for easy looping over later - must move each square & center point in tandem
        self._to_move = list(self.squares)
        self._to_move.append(self.center)

    def has_square_at(self, p: Point) -> bool:
        return p.pos in [sq.pos for sq in self.squares]

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
            y_dist = sq.row() - self.center.row()
            x_dist = sq.col() - self.center.col()

            # swap y and x distances
            if clockwise:
                new_x = self.center.col() - y_dist
                new_y = self.center.row() + x_dist
            else:
                new_x = self.center.col() + y_dist
                new_y = self.center.row() - x_dist

            sq.teleport((new_y, new_x))

    def remove_row(self, row: int) -> List[Block]:
        print('My squares are at', [sq.pos for sq in self.squares], 'and once I remove those in row', row,
              "I'm left with", [sq.pos for sq in self.squares if sq.pos[0] != row], 'and the groups will be',
              [[sq.pos for sq in group]
               for group in find_connected_groups([sq for sq in self.squares if sq.pos[0] != row])])
        return [Block(colors.BROKEN_PIECE_COLOR, [sq.pos for sq in group], group[0].pos)
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

    return Block(colors.SHADOW_COLOR, [sq.pos for sq in original.squares], original.center.pos)

def find_connected_groups(points: List[Point]) -> List[List[Point]]:
    """Find connected groups of Points"""

    # create a graph of points: adj points, but only map if there are adj sqs
    adj_graph: Dict[Point, List[Point]] = {point: adjs for point in points
                                           if (adjs := [adj for adj in points if are_adj(point, adj)])}
    # graph of points to which group they're in
    points_to_groups = dict()
    # initialize each point to own group
    groups = [[point] for point in points]
    for i in range(len(points)):
        points_to_groups[points[i]] = i

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
def _make_I_block(O_bottom_left: Tuple[int, int]) -> Block:
    return Block(colors.I_COLOR, [(O_bottom_left[0], O_bottom_left[1] - i + 1) for i in range(4)],
                 (O_bottom_left[0] + 0.5, O_bottom_left[1] - 0.5))

def _make_O_block(O_bottom_left: Tuple[int, int]) -> Block:
    return Block(colors.O_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j) for i in range(2) for j in range(2)],
                 (O_bottom_left[0] - 0.5, O_bottom_left[0] - 0.5))

def _make_T_block(O_bottom_left: Tuple[int, int]) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1]))
    return Block(colors.T_COLOR, straight, O_bottom_left)

def _make_S_block(O_bottom_left: Tuple[int, int]) -> Block:
    return Block(colors.S_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j + 1 - i)
                                  for i in range(2) for j in range(2)], O_bottom_left)

def _make_Z_block(O_bottom_left: Tuple[int, int]) -> Block:
    return Block(colors.Z_COLOR, [(O_bottom_left[0] - i, O_bottom_left[1] - j + i)
                                  for i in range(2) for j in range(2)], O_bottom_left)

def _make_J_block(O_bottom_left: Tuple[int, int]) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1] + 1))
    return Block(colors.J_COLOR, straight, O_bottom_left)

def _make_L_block(O_bottom_left: Tuple[int, int]) -> Block:
    straight = [(O_bottom_left[0], O_bottom_left[1] + 1 - i) for i in range(3)]
    straight.append((O_bottom_left[0] - 1, O_bottom_left[1] - 1))
    return Block(colors.L_COLOR, straight, O_bottom_left)

def random_block(columns: int) -> Block:
    """Create a random standard Tetris piece in the middle of the top of the field"""
    return random.choice((_make_I_block, _make_O_block, _make_T_block, _make_S_block,
                          _make_Z_block, _make_J_block, _make_L_block))((0, int(columns / 2)))


if __name__ == '__main__':
    groups = find_connected_groups([Point((0,1)), Point((1,1))])
    for i in range(len(groups)):
        print('group', i + 1, [point.pos for point in groups[i]])
