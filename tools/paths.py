"""
Tools for manipulating spatial paths
"""
from enum import Enum
from math import fabs


class CardinalPoint(Enum):
    """
    A point on the compass
    """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


class TurnDirection(Enum):
    """
    A clockwise (right) or counterclockwise (left) rotation
    """
    LEFT = 0
    RIGHT = 1


def flip_direction(direction: TurnDirection):
    """
    Utility method to flip the direction of a rotation
    """
    if direction == TurnDirection.LEFT:
        result = TurnDirection.RIGHT
    elif direction == TurnDirection.RIGHT:
        result = TurnDirection.LEFT
    else:
        raise ValueError
    return result


def turn(cardinal: CardinalPoint, direction: TurnDirection, degrees: int):
    """
    Given a body is currently pointed in the direction specified by
    cardinal - return the direction it will be pointed to after a
    a rotation of <degrees> in <direction>.

    The rotation must alight on a valid CardinalPoint, else a
    ValueError will be thrown

    :return: The Cardinal point the body is now pointed
    """
    if direction == TurnDirection.LEFT:
        result = cardinal.value - degrees
    elif direction == TurnDirection.RIGHT:
        result = cardinal.value + degrees
    else:
        raise ValueError

    return CardinalPoint(result % 360)


class Point:
    """
    Represents a point in cartesian space
    """

    def __init__(self, x_coord, y_coord):
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord

    def manhattan_distance(self):
        """
        Compute the distance between two points if you go around both side of the triangle
        """
        return fabs(self.x_coordinate) + fabs(self.y_coordinate)

    def __eq__(self, other):
        return self.x_coordinate == other.x_coordinate and self.y_coordinate == other.y_coordinate

    def __str__(self):
        return "(" + str(self.x_coordinate) + "," + str(self.y_coordinate) + ")"

    def __lt__(self, other):
        if self.x_coordinate == other.x_coordinate:
            less_than = self.y_coordinate < other.y_coordinate
        else:
            less_than = self.x_coordinate < other.x_coordinate
        return less_than

    def __repr__(self):
        return self.__str__()


class PathPoint:
    """
    A point (in cartesian space) along a vector path
    """

    def __init__(self, x_coord, y_coord, length):
        self.point = Point(x_coord, y_coord)
        self.path_len = length

    def get_point(self):
        """
        Access the point in space
        """
        return self.point

    def __eq__(self, other):
        return self.point == other.point and self.path_len == other.path_len

    def __lt__(self, other):
        if self.path_len == other.path_len:
            less_than = self.point < other.point
        else:
            less_than = self.path_len < other.path_len
        return less_than

    def __str__(self):
        return "[" + str(self.path_len) + "]: " + self.point.__str__()

    def __repr__(self):
        return self.__str__()


def make_path_from_vectors(vectors: list, direction: CardinalPoint = None):
    """
    Wraps max_path to allow a whole sequence of path steps,
    e.g explicit directions:
       ["U2", "L3", "D1", "U2"]
    if the optional <direction> argument has been provided, then additional
    commands are accepted:
       C: Turn counter clock-wise
       A: Turn counter counter-clock-wise
       F: Go forward in the direction of the cardinal point (Up = NORTH)
    """
    origin = PathPoint(0, 0, 0)
    path = [origin]
    for vec in vectors:
        if vec[0] == "C":
            direction = turn(direction, TurnDirection.RIGHT, int(vec[1:]))
        elif vec[0] == "A":
            direction = turn(direction, TurnDirection.LEFT, int(vec[1:]))
        else:
            line = make_path(path[-1], vec, direction)
            path += line[1:]

    return path


def make_path(origin: PathPoint, code: str, direction: CardinalPoint = None):
    """
    Create a path from origin to a point defined relative to origin
    by a string instruction of the form:
        <U|D|L|R><length>
    e.g
        U4: Up (+'ve y axis) 4 points
        D3: Down (-'ve y axis) 3 points
        R4: LEFT (+'ve x axis) 4 points
        L3: RIGHT (-'ve x axis) 3 points
        F3: Go forward (U/D/L/R bases on the provided cardinal point)
    """
    path = [origin]
    if len(code) > 0:
        delta_x = 0
        delta_y = 0
        path_len = int(code[1:])
        letter = code[0]
        is_forward = letter == "F"
        if letter == "R" or (is_forward and direction == CardinalPoint.EAST):
            delta_x = 1
        elif letter == "L" or (is_forward and direction == CardinalPoint.WEST):
            delta_x = -1
        elif letter == "U" or (is_forward and direction == CardinalPoint.NORTH):
            delta_y = 1
        elif letter == "D" or (is_forward and direction == CardinalPoint.SOUTH):
            delta_y = -1

        for i in range(1, path_len + 1):
            path.append(
                PathPoint(
                    origin.point.x_coordinate + i * delta_x,
                    origin.point.y_coordinate + i * delta_y,
                    origin.path_len + i))
    return path


def rotate(origin: Point, point: Point, direction: TurnDirection, degrees: int):
    """
    Rotate The point (point) by (degrees) degrees around the origin point (origin)

    :param origin:    The point to rotate around
    :param point:     The point to rotate
    :param direction: RIGHT (clockwise) or LEFT (counter-clockwise)
    :param degrees:   90, 180 or 270

    :return: The rotated Point
    """
    coordinate_x = point.x_coordinate - origin.x_coordinate
    coordinate_y = point.y_coordinate - origin.y_coordinate

    if degrees == 0:
        pass
    elif degrees == 180:
        coordinate_x *= -1
        coordinate_y *= -1
    elif degrees in (90, 270):
        if degrees == 270:
            direction = flip_direction(direction)

        if direction == TurnDirection.RIGHT:
            coordinate_x, coordinate_y = coordinate_y, -coordinate_x
        elif direction == TurnDirection.LEFT:
            coordinate_x, coordinate_y = -coordinate_y, coordinate_x
        else:
            raise ValueError
    else:
        raise ValueError

    return Point(origin.x_coordinate + coordinate_x, origin.y_coordinate + coordinate_y)


def sort_by_manhattan_distance(path: list):
    """
    Utility function to sort a list of paths, by their manhattan_distance...
    """
    path.sort(key=lambda obj: obj.manhattan_distance())
