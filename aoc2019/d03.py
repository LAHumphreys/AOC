from tools.fileLoader import LoadLists
from tools.listOps import NonSortedMatchGroups, NonSortedIntersection
from tools.paths import MakePathFromVectors, Point, PathPoint

def FindNearestIntsection(pathVectorsA, pathVectorsB):
    pathA = MakePathFromVectors(pathVectorsA)[1:]
    pathB = MakePathFromVectors(pathVectorsB)[1:]

    key = lambda p: p.GetPoint()

    intersects = NonSortedIntersection(pathA, pathB, key=key)

    if len(intersects) > 0:
        distSort = lambda p: p.GetPoint().ManhattanDistance()
        intersects.sort(key=distSort)
        return intersects[0]
    else:
        return None

def FindShortestIntersection(pathVectorsA, pathVectorsB):
    pathA = MakePathFromVectors(pathVectorsA)[1:]
    pathB = MakePathFromVectors(pathVectorsB)[1:]

    key = lambda p: p.GetPoint()

    groups = NonSortedMatchGroups(pathA, pathB, key=key)

    if len (groups) > 0:
        pathLenSort = lambda p: p.pathLen

        class Result:
            def __init__(self, A: PathPoint, B: PathPoint):
                self.pointA = A
                self.pointB = B
                self.pathLen = A.pathLen + B.pathLen

        results = []

        for group in groups:
            intsectsA = group[0]
            intsectsB = group[1]

            intsectsA.sort(key=pathLenSort)
            intsectsB.sort(key=pathLenSort)

            results.append(Result(intsectsA[0], intsectsB[0]))

        results.sort(key=pathLenSort)

        return results[0]

    else:
        return None



if __name__ == "__main__":
    [pathVectorsA, pathVectorsB] = LoadLists("input/d03.txt")
    print (FindNearestIntsection(pathVectorsA, pathVectorsB))
    print (FindShortestIntersection(pathVectorsA, pathVectorsB).pathLen)
