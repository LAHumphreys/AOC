from unittest import TestCase
from aoc2025.d07 import load_sample, part1, propagate_tachyon, display_paths
from aoc2025.d07 import  part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay07(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d07.txt")
        self.data = load_sample(self.sample_path)

    def test_step_one(self):
        print(display_paths(self.data))
        splits = propagate_tachyon(self.data, 1)
        print(display_paths(self.data))
        self.assertEqual(splits, 0)

    def test_step_two(self):
        print(display_paths(self.data))
        splits = propagate_tachyon(self.data, 1)
        display_paths(self.data)
        splits += propagate_tachyon(self.data, 2)
        display_paths(self.data)
        self.assertEqual(splits, 1)

    def test_part_one(self):
        self.assertEqual(part1(self.data), 21)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 0)
