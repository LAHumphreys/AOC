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

    def __lt__(self, other):
        if (self.x == other.x):
            return self.y < other.y
        else:
            return self.x < other.x

    def __repr__(self):
        return self.__str__()

class PathPoint:
    def __init__(self, x, y, len):
        self.point = Point(x,y)
        self.pathLen = len

    def GetPoint(self):
        return self.point

    def __eq__(self, other):
        return self.point == other.point  and self.pathLen == other.pathLen

    def __lt__(self, other):
        if self.pathLen == other.pathLen:
            return self.point < other.point
        else:
            return self.pathLen < other.pathLen

    def __str__(self):
        return "[" + str(self.pathLen) + "]: " + self.point.__str__()

    def __repr__(self):
        return self.__str__()

def MakePathFromVectors(vectors:list):
    origin = PathPoint(0,0,0)
    path = [origin]
    for vec in vectors:
        line = MakePath(path[-1], vec)
        path += line[1:]

    return path


def MakePath(origin: PathPoint, code: str):
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
            path.append(PathPoint(origin.point.x+i*dx, origin.point.y + i*dy, origin.pathLen + i))
    return path


def SortByManhattanDistance(path: list):
    key = lambda obj: obj.ManhattanDistance()
    path.sort(key=key)