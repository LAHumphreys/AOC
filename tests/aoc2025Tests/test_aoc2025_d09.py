from unittest import TestCase
from aoc2025.d09 import load_sample, part1, part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay09(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d09.txt")
        self.data = load_sample(self.sample_path)

    def test_part_one(self):
        self.assertEqual(part1(self.data), 50)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 0)
