from math import fabs
class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def ManhattanDistance(self):
        return fabs(self.x) + fabs(self.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

def MakePathFromVectors(vectors:list):
    origin = Point(0,0)
    path = [origin]
    for vec in vectors:
        line = MakePath(path[-1], vec)
        path += line[1:]

    return path


def MakePath(origin: Point, code: str):
    path = [origin]
    if len(code) > 0:
        dx = 0
        dy = 0
        pathLen = int(code[1:])
        if code[0] == "R":
            dx = 1
        elif code[0] == "L":
            dx = -1
        elif code[0] == "U":
            dy = 1
        elif code[0] == "D":
            dy = -1

        for i in range(1,pathLen+1):
            path.append(Point(origin.x+i*dx, origin.y + i*dy))
    return path


def SortByManhattanDistance(path: list):
    key = lambda obj: obj.ManhattanDistance()
    path.sort(key=key)