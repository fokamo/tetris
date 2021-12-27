"""point.py - for a Point class

For external use:
- Point class for representing a movable point
- are_adj_points(one: Point, two: Point) -> bool function for checking if points are orthogonally 1 unit apart
"""

from typing import Tuple

class Point:
    """A point in space

    For external use:
    - .pos is (row, col) position
    - .row() -> float and .col() -> float to get such position information
    - .down(), .up(), .left(), and .right() to move the Point 1 unit in such direction
    - .teleport(new_pos: Tuple[float, float]) to move the Point to a specified location
    - .__eq__(other), .__ne__(other), .__hash__(), and .__str__() overridden
    """

    def __init__(self, pos: Tuple[float, float]) -> None:
        # (row, col), right & down are greater
        self.pos = pos

    # position getters
    def row(self) -> float:
        return self.pos[0]

    def col(self) -> float:
        return self.pos[1]

    # aliases for _move() for outside use
    def down(self) -> None:
        self._move(1, 0)

    def up(self) -> None:
        self._move(-1, 0)

    def left(self) -> None:
        self._move(0, -1)

    def right(self) -> None:
        self._move(0, 1)

    def _move(self, row_move, col_move):
        self.pos = (self.pos[0] + row_move, self.pos[1] + col_move)

    # for move complicated movements - use with caution
    def teleport(self, new_pos: Tuple[float, float]) -> None:
        self.pos = new_pos

    # overriding comparison methods
    def __eq__(self, other) -> bool:
        return isinstance(other, Point) and self.pos == other.pos

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.pos)

    # for debugging, mostly
    def __str__(self) -> str:
        return str(self.pos)

def are_adj_points(one: Point, two: Point) -> bool:
    """Check if two Points are orthogonally adjacent to each other"""

    if one.row() == two.row():
        # horizontal adjacency
        return abs(one.col() - two.col()) == 1
    elif one.col() == two.col():
        # vertical adjacency
        return abs(one.row() - two.row()) == 1

    return False
