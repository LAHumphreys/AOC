from unittest import TestCase
from aoc2025.d08 import load_sample, part1, find_nearest, Point
from aoc2025.d08 import  part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay08(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d08.txt")
        self.data = load_sample(self.sample_path)

    def test_find_nearest(self):
        nearest = find_nearest(self.data[0], self.data)
        self.assertEqual(nearest, Point(425, 690, 689))
        pass

    def test_part_one(self):
        self.assertEqual(part1(self.data, 10), 40)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 25272)
