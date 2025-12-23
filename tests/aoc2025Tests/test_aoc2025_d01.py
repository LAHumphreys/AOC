from unittest import TestCase
from aoc2025.d01 import apply_rotation, load_sample, part1, part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay01(TestCase):
    def setUp(self):
        self.lines = load_sample(get_test_file_path("samples/d01.txt"))

    def test_direction(self):
        self.assertEqual(apply_rotation(50, "L68"), 82)
        self.assertEqual(apply_rotation(52, "R48"), 0)
        self.assertEqual(apply_rotation(52, "R60"), 12)

    def test_part_one(self):
        self.assertEqual(part1(self.lines), 3)

    def test_part_two(self):
        self.assertEqual(part2(self.lines), 6)
