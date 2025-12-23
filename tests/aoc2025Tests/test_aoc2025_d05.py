from unittest import TestCase
from aoc2025.d05 import load_sample, part1, part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay05(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d05.txt")
        self.data = load_sample(self.sample_path)

    def test_part_one(self):
        self.assertEqual(part1(self.data), 3)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 14)
