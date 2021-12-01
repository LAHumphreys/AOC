from unittest import TestCase

from tools.paths import CardinalPoint, TurnDirection, turn, rotate
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

    def test_north_then_east(self):
        vectors = ["F2", "C90", "F3"]
        expected = [
            PathPoint(0, 0, 0), PathPoint(0, 1, 1), PathPoint(0, 2, 2),
            PathPoint(1, 2, 3), PathPoint(2, 2, 4), PathPoint(3, 2, 5)]
        cardinal = CardinalPoint.NORTH
        path = make_path_from_vectors(vectors, cardinal)
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

    def test_south_then_east(self):
        vectors = ["F2", "A90", "F3"]
        expected = [
            PathPoint(0, 0, 0), PathPoint(0, -1, 1), PathPoint(0, -2, 2),
            PathPoint(1, -2, 3), PathPoint(2, -2, 4), PathPoint(3, -2, 5)]
        cardinal = CardinalPoint.SOUTH
        path = make_path_from_vectors(vectors, cardinal)
        self.assertListEqual(path, expected)


class TestPath(TestCase):

    def test_EmptyPath(self):
        origin = PathPoint(0, 0, 0)
        self.assertListEqual(make_path(origin, ""), [origin])

    def test_RIGHT(self):
        origin = PathPoint(0, 0, 0)
        result = [
            origin, PathPoint(
                1, 0, 1), PathPoint(
                2, 0, 2), PathPoint(
                3, 0, 3), PathPoint(
                4, 0, 4), PathPoint(
                5, 0, 5)]
        self.assertListEqual(make_path(origin, "R5"), result)

    def test_EAST(self):
        origin = PathPoint(0, 0, 0)
        result = [
            origin, PathPoint(
                1, 0, 1), PathPoint(
                2, 0, 2), PathPoint(
                3, 0, 3), PathPoint(
                4, 0, 4), PathPoint(
                5, 0, 5)]
        self.assertListEqual(make_path(origin, "F5", CardinalPoint.EAST), result)

    def test_LEFT(self):
        origin = PathPoint(2, 0, 0)
        result = [
            origin, PathPoint(1, 0, 1),
            PathPoint(0, 0, 2),
            PathPoint(-1, 0, 3),
            PathPoint(-2, 0, 4),
            PathPoint(-3, 0, 5)]
        self.assertListEqual(make_path(origin, "L5"), result)

    def test_WEST(self):
        origin = PathPoint(2, 0, 0)
        result = [
            origin, PathPoint(1, 0, 1),
            PathPoint(0, 0, 2),
            PathPoint(-1, 0, 3),
            PathPoint(-2, 0, 4),
            PathPoint(-3, 0, 5)]
        self.assertListEqual(make_path(origin, "F5", CardinalPoint.WEST), result)

    def test_Up(self):
        origin = PathPoint(-2, -3, 0)
        result = [
            origin, PathPoint(-2, -2, 1),
            PathPoint(-2, -1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, 1, 4),
            PathPoint(-2, 2, 5)]
        self.assertListEqual(make_path(origin, "U5"), result)

    def test_NORTH(self):
        origin = PathPoint(-2, -3, 0)
        result = [
            origin, PathPoint(-2, -2, 1),
            PathPoint(-2, -1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, 1, 4),
            PathPoint(-2, 2, 5)]
        self.assertListEqual(make_path(origin, "F5", CardinalPoint.NORTH), result)

    def test_Down(self):
        origin = PathPoint(-2, 3, 0)
        result = [
            origin, PathPoint(-2, 2, 1),
            PathPoint(-2, 1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, -1, 4),
            PathPoint(-2, -2, 5)]
        self.assertListEqual(make_path(origin, "D5"), result)

    def test_SOUTH(self):
        origin = PathPoint(-2, 3, 0)
        result = [
            origin, PathPoint(-2, 2, 1),
            PathPoint(-2, 1, 2),
            PathPoint(-2, 0, 3),
            PathPoint(-2, -1, 4),
            PathPoint(-2, -2, 5)]
        self.assertListEqual(make_path(origin, "F5", CardinalPoint.SOUTH), result)


class TestCardinalTurning(TestCase):
    def test_TurnNowhere(self):
        self.assertEqual(CardinalPoint.NORTH, turn(CardinalPoint.NORTH, TurnDirection.LEFT, 0))
        self.assertEqual(CardinalPoint.NORTH, turn(CardinalPoint.NORTH, TurnDirection.RIGHT, 0))
        self.assertEqual(CardinalPoint.EAST, turn(CardinalPoint.EAST, TurnDirection.LEFT, 0))
        self.assertEqual(CardinalPoint.EAST, turn(CardinalPoint.EAST, TurnDirection.RIGHT, 0))
        self.assertEqual(CardinalPoint.WEST, turn(CardinalPoint.WEST, TurnDirection.LEFT, 0))
        self.assertEqual(CardinalPoint.WEST, turn(CardinalPoint.WEST, TurnDirection.RIGHT, 0))
        self.assertEqual(CardinalPoint.SOUTH, turn(CardinalPoint.SOUTH, TurnDirection.LEFT, 0))
        self.assertEqual(CardinalPoint.SOUTH, turn(CardinalPoint.SOUTH, TurnDirection.RIGHT, 0))

    def test_TurnUnknownAmount(self):
        self.assertRaises(ValueError, lambda: turn(CardinalPoint.NORTH, TurnDirection.RIGHT, 25))

    def test_TurnRIGHT(self):
        self.assertEqual(CardinalPoint.EAST, turn(CardinalPoint.NORTH, TurnDirection.RIGHT, 90))
        self.assertEqual(CardinalPoint.NORTH, turn(CardinalPoint.WEST, TurnDirection.RIGHT, 90))
        self.assertEqual(CardinalPoint.EAST, turn(CardinalPoint.WEST, TurnDirection.RIGHT, 180))
        self.assertEqual(CardinalPoint.WEST, turn(CardinalPoint.EAST, TurnDirection.RIGHT, 180))
        self.assertEqual(CardinalPoint.SOUTH, turn(CardinalPoint.NORTH, TurnDirection.RIGHT, 180))
        self.assertEqual(CardinalPoint.NORTH, turn(CardinalPoint.SOUTH, TurnDirection.RIGHT, 180))

    def test_TurnLEFT(self):
        self.assertEqual(CardinalPoint.SOUTH, turn(CardinalPoint.WEST, TurnDirection.LEFT, 90))
        self.assertEqual(CardinalPoint.WEST, turn(CardinalPoint.NORTH, TurnDirection.LEFT, 90))
        self.assertEqual(CardinalPoint.EAST, turn(CardinalPoint.SOUTH, TurnDirection.LEFT, 90))
        self.assertEqual(CardinalPoint.WEST, turn(CardinalPoint.EAST, TurnDirection.LEFT, 180))
        self.assertEqual(CardinalPoint.NORTH, turn(CardinalPoint.SOUTH, TurnDirection.LEFT, 180))
        self.assertEqual(CardinalPoint.SOUTH, turn(CardinalPoint.NORTH, TurnDirection.LEFT, 180))


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


class TestRotate(TestCase):
    def test_unit_no_turn(self):
        origin = Point(0, 0)
        up = Point(0, 1)
        down = Point(0, -1)
        left = Point(-1, 0)
        right = Point(1, 0)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(up, rotate(origin, up, clockwise, 0))
        self.assertEqual(down, rotate(origin, down, clockwise, 0))
        self.assertEqual(left, rotate(origin, left, clockwise, 0))
        self.assertEqual(right, rotate(origin, right, clockwise, 0))

    def test_unit_180(self):
        origin = Point(0, 0)
        up = Point(0, 1)
        down = Point(0, -1)
        left = Point(-1, 0)
        right = Point(1, 0)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(down, rotate(origin, up, clockwise, 180))
        self.assertEqual(up, rotate(origin, down, clockwise, 180))
        self.assertEqual(right, rotate(origin, left, clockwise, 180))
        self.assertEqual(left, rotate(origin, right, clockwise, 180))
        self.assertEqual(down, rotate(origin, up, counterclockwise, 180))
        self.assertEqual(up, rotate(origin, down, counterclockwise, 180))
        self.assertEqual(right, rotate(origin, left, counterclockwise, 180))
        self.assertEqual(left, rotate(origin, right, counterclockwise, 180))

    def test_unit_90(self):
        origin = Point(0, 0)
        up = Point(0, 1)
        down = Point(0, -1)
        left = Point(-1, 0)
        right = Point(1, 0)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(right, rotate(origin, up, clockwise, 90))
        self.assertEqual(left, rotate(origin, down, clockwise, 90))
        self.assertEqual(up, rotate(origin, left, clockwise, 90))
        self.assertEqual(down, rotate(origin, right, clockwise, 90))
        self.assertEqual(left, rotate(origin, up, counterclockwise, 90))
        self.assertEqual(right, rotate(origin, down, counterclockwise, 90))
        self.assertEqual(down, rotate(origin, left, counterclockwise, 90))
        self.assertEqual(up, rotate(origin, right, counterclockwise, 90))

    def test_unit_270(self):
        origin = Point(0, 0)
        up = Point(0, 1)
        down = Point(0, -1)
        left = Point(-1, 0)
        right = Point(1, 0)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(right, rotate(origin, up, counterclockwise, 270))
        self.assertEqual(left, rotate(origin, down, counterclockwise, 270))
        self.assertEqual(up, rotate(origin, left, counterclockwise, 270))
        self.assertEqual(down, rotate(origin, right, counterclockwise, 270))
        self.assertEqual(left, rotate(origin, up, clockwise, 270))
        self.assertEqual(right, rotate(origin, down, clockwise, 270))
        self.assertEqual(down, rotate(origin, left, clockwise, 270))
        self.assertEqual(up, rotate(origin, right, clockwise, 270))

    def test_off_axis(self):
        origin = Point(0, 0)
        start = Point(4, 1)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(Point(1, -4), rotate(origin, start, clockwise, 90))
        self.assertEqual(Point(-1, 4), rotate(origin, start, counterclockwise, 90))

    def test_off_axis_off_origin(self):
        origin = Point(2, 2)
        start = Point(6, 3)
        clockwise = TurnDirection.RIGHT
        counterclockwise = TurnDirection.LEFT
        self.assertEqual(Point(3, -2), rotate(origin, start, clockwise, 90))
        self.assertEqual(Point(1, 6), rotate(origin, start, counterclockwise, 90))

    def test_example(self):
        origin = Point(0, 0)
        start = Point(10, 4)
        final = Point(4, -10)
        clockwise = TurnDirection.RIGHT
        self.assertEqual(final, rotate(origin, start, clockwise, 90))
