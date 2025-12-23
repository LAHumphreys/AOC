from unittest import TestCase
from aoc2025.d01 import part1, part2


class TestDay01(TestCase):
    def test_part1(self):
        self.assertEqual(part1(["line1", "line2"]), 2)

    def test_part2(self):
        self.assertEqual(part2(["line1", "line2"]), 2)
