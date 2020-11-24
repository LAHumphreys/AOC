from tools.paths import Point, MakePath, SortByManhattanDistance, MakePathFromVectors
from unittest import TestCase


class TestPoint(TestCase):
    def test_Manhattan(self):
        self.assertEqual(Point(0,0).ManhattanDistance(), 0)
        self.assertEqual(Point(0,1).ManhattanDistance(), 1)
        self.assertEqual(Point(2,2).ManhattanDistance(), 4)
        self.assertEqual(Point(3,2).ManhattanDistance(), 5)
        self.assertEqual(Point(-3,2).ManhattanDistance(), 5)


class TestPathFromVectors(TestCase):

    def test_UR(self):
        vectors = ["U2", "R3"]
        expected = [Point(0,0), Point(0,1), Point(0,2), Point(1,2), Point(2,2), Point(3,2)]
        path = MakePathFromVectors(vectors)
        self.assertListEqual(path, expected)

    def test_DL(self):
        vectors = ["D2", "L3"]
        expected = [Point(0,0), Point(0,-1), Point(0,-2), Point(-1,-2), Point(-2,-2), Point(-3,-2)]
        path = MakePathFromVectors(vectors)
        self.assertListEqual(path, expected)


class TestPath(TestCase):

    def test_EmptyPath(self):
        origin = Point(0,0)
        self.assertListEqual(MakePath(origin, ""), [origin])

    def test_Right(self):
        origin = Point(0,0)
        result = [origin, Point(1,0), Point(2,0), Point(3,0), Point(4,0), Point(5,0)]
        self.assertListEqual(MakePath(origin, "R5"), result)

    def test_Left(self):
        origin = Point(2,0)
        result = [origin, Point(1,0), Point(0,0), Point(-1,0), Point(-2,0), Point(-3,0)]
        self.assertListEqual(MakePath(origin, "L5"), result)

    def test_Up(self):
        origin = Point(-2,-3)
        result = [origin, Point(-2,-2), Point(-2,-1), Point(-2,0), Point(-2,1), Point(-2,2)]
        self.assertListEqual(MakePath(origin, "U5"), result)

    def test_Down(self):
        origin = Point(-2,3)
        result = [origin, Point(-2,2), Point(-2,1), Point(-2,0), Point(-2,-1), Point(-2,-2)]
        self.assertListEqual(MakePath(origin, "D5"), result)

class TestManhattanSort(TestCase):
    def test_xaxis(self):
        path = [Point(1,0), Point(-2,0), Point(0,0), Point(-1,0)]
        SortByManhattanDistance(path)
        self.assertListEqual(path, [Point(0,0), Point(1,0), Point(-1,0), Point(-2,0)])

    def test_yaxis(self):
        path = [Point(0,1), Point(0,-2), Point(0,0), Point(0,-1)]
        SortByManhattanDistance(path)
        self.assertListEqual(path, [Point(0,0), Point(0,1), Point(0,-1), Point(0,-2)])
