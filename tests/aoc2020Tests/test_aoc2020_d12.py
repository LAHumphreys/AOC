from unittest import TestCase

from aoc2020.d12 import convert_to_std, load_direction, make_ship_path, move_by_waypoint
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath
from tools.paths import Point


class Conversion(TestCase):
    def test_all_directions(self):
        advent_format = ["N1", "S2", "E3", "W4", "L90", "R180", "F10"]
        tools_format = ["U1", "D2", "R3", "L4", "A90", "C180", "F10"]
        self.assertListEqual(tools_format, convert_to_std(advent_format))


class PartOne(TestCase):
    def test_part_one(self):
        path = GetTestFilePath("samples/d12/sample1.txt")
        directions = load_direction(path)
        result = make_ship_path(directions)
        self.assertEqual(result[-1].get_point().manhattan_distance(), 25)


class PartTwo(TestCase):
    def test_move_by_waypoint_forward(self):
        directions = ["F10"]
        end_point = move_by_waypoint(directions)
        self.assertEqual(end_point, Point(100, 10))

    def test_move_by_waypoint_step_two(self):
        directions = ["F10", "U3"]
        end_point = move_by_waypoint(directions)
        self.assertEqual(end_point, Point(100, 10))

    def test_move_by_waypoint_step_three(self):
        directions = ["F10", "U3", "F7"]
        end_point = move_by_waypoint(directions)
        self.assertEqual(end_point, Point(170, 38))

    def test_move_by_waypoint_step_four(self):
        directions = ["F10", "U3", "F7", "C90"]
        end_point = move_by_waypoint(directions)
        self.assertEqual(end_point, Point(170, 38))

    def test_move_by_waypoint_step_five(self):
        directions = ["F10", "U3", "F7", "C90", "F11"]
        end_point = move_by_waypoint(directions)
        self.assertEqual(end_point, Point(214, -72))
