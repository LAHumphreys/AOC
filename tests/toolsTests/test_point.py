from unittest import TestCase

from tools.paths import Point, make_path, sort_by_manhattan_distance, make_path_from_vectors, PathPoint


class TestPoint(TestCase):
    def test_Manhattan(self):
        self.assertEqual(Point(0, 0).manhattan_distance(), 0)
        self.assertEqual(Point(0, 1).manhattan_distance(), 1)
        self.assertEqual(Point(2, 2).manhattan_distance(), 4)
        self.assertEqual(Point(3, 2).manhattan_distance(), 5)
        self.assertEqual(Point(-3, 2).manhattan_distance(), 5)


class TestPathFromVectors(TestCase):

    def test_UR(self):
        vectors = ["U2", "R3"]
        expected = [
            PathPoint(
                0, 0, 0), PathPoint(
                0, 1, 1), PathPoint(
                0, 2, 2), PathPoint(
                1, 2, 3), PathPoint(
                2, 2, 4), PathPoint(
                3, 2, 5)]
        path = make_path_from_vectors(vectors)
        self.assertListEqual(path, expected)

    def test_DL(self):
        vectors = ["D2", "L3"]
        expected = [
            PathPoint(0, 0, 0),
            PathPoint(0, -1, 1),
            PathPoint(0, -2, 2),
            PathPoint(-1, -2, 3),
            PathPoint(-2, -2, 4),
            PathPoint(-3, -2, 5)]
        path = make_path_from_vectors(vectors)
        self.assertListEqual(path, expected)


class TestPath(TestCase):

    def test_EmptyPath(self):
        origin = PathPoint(0, 0, 0)
        self.assertListEqual(make_path(origin, ""), [origin])

    def test_Right(self):
        origin = PathPoint(0, 0, 0)
        result = [
            origin, PathPoint(
                1, 0, 1), PathPoint(
                2, 0, 2), PathPoint(
                3, 0, 3), PathPoint(
                4, 0, 4), PathPoint(
                5, 0, 5)]
        self.assertListEqual(make_path(origin, "R5"), result)

    def test_Left(self):
        origin = PathPoint(2, 0, 0)
        result = [
            origin, PathPoint(1, 0, 1),
            PathPoint(0, 0, 2),
            PathPoint(-1, 0, 3),
            PathPoint(-2, 0, 4),
            PathPoint(-3, 0, 5)]
        self.assertListEqual(make_path(origin, "L5"), result)

    def test_Up(self):
        origin = PathPoint(-2, -3, 0)
        result = [
            origin, PathPoint(-2, -2, 1),
            PathPoint(-2, -1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, 1, 4),
            PathPoint(-2, 2, 5)]
        self.assertListEqual(make_path(origin, "U5"), result)

    def test_Down(self):
        origin = PathPoint(-2, 3, 0)
        result = [
            origin, PathPoint(-2, 2, 1),
            PathPoint(-2, 1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, -1, 4),
            PathPoint(-2, -2, 5)]
        self.assertListEqual(make_path(origin, "D5"), result)


class TestManhattanSort(TestCase):
    def test_xaxis(self):
        path = [Point(1, 0), Point(-2, 0), Point(0, 0), Point(-1, 0)]
        sort_by_manhattan_distance(path)
        self.assertListEqual(
            path, [Point(0, 0), Point(1, 0), Point(-1, 0), Point(-2, 0)])

    def test_yaxis(self):
        path = [Point(0, 1), Point(0, -2), Point(0, 0), Point(0, -1)]
        sort_by_manhattan_distance(path)
        self.assertListEqual(
            path, [Point(0, 0), Point(0, 1), Point(0, -1), Point(0, -2)])
