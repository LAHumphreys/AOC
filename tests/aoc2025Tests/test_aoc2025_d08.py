from unittest import TestCase
from aoc2025.d08 import load_sample, part1, find_nearest, Point, map_points, make_circuits
from aoc2025.d08 import  part2, make_connection
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay08(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d08.txt")
        self.data = load_sample(self.sample_path)

    def test_find_nearest(self):
        nearest = find_nearest(self.data[0], self.data)
        self.assertEqual(nearest, Point(425, 690, 689))
        pass

    def test_map_points(self):
        connection_map = map_points(self.data)

        # Test that all points have a nearest neighbor
        self.assertEqual(len(connection_map.neighbours), len(self.data))

        # Test that the first point's neighbor is correct
        self.assertEqual(connection_map.neighbours[self.data[0]], Point(425, 690, 689))

        # Test that connection distances are positive
        for conn in connection_map.possible_connections:
            self.assertGreater(conn.distance, 0)

    def test_part_one(self):
        self.assertEqual(part1(self.data, 10), 40)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 0)
