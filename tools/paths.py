"""
Tools for manipulating spatial paths
"""
from math import fabs


class Point:
    """
    Represents a point in cartesian space
    """

    def __init__(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

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

    def __init__(self, x, y, length):
        self.point = Point(x, y)
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


def make_path_from_vectors(vectors: list):
    """
    Wraps max_path to allow a whole sequence of path steps,
    e.g:
       ["U2", "L3", "D1", "U2"]
    """
    origin = PathPoint(0, 0, 0)
    path = [origin]
    for vec in vectors:
        line = make_path(path[-1], vec)
        path += line[1:]

    return path


def make_path(origin: PathPoint, code: str):
    """
    Create a path from origin to a point defined relative to origin
    by a string instruction of the form:
        <U|D|L|R><length>
    e.g
        U4: Up (+'ve y axis) 4 points
        D3: Down (-'ve y axis) 3 points
        R4: Left (+'ve x axis) 4 points
        L3: Right (-'ve x axis) 3 points
    """
    path = [origin]
    if len(code) > 0:
        delta_x = 0
        delta_y = 0
        path_len = int(code[1:])
        if code[0] == "R":
            delta_x = 1
        elif code[0] == "L":
            delta_x = -1
        elif code[0] == "U":
            delta_y = 1
        elif code[0] == "D":
            delta_y = -1

        for i in range(1, path_len + 1):
            path.append(
                PathPoint(
                    origin.point.x_coordinate + i * delta_x,
                    origin.point.y_coordinate + i * delta_y,
                    origin.path_len + i))
    return path


def sort_by_manhattan_distance(path: list):
    """
    Utility function to sort a list of paths, by their manhattan_distance...
    """
    path.sort(key=lambda obj: obj.manhattan_distance())
