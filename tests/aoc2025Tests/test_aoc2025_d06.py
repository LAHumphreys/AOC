from unittest import TestCase
from aoc2025.d06 import load_sample, part1, solve_part_one
from aoc2025.d06 import  part2, solve_part_two
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay06(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d06.txt")
        self.data = load_sample(self.sample_path)

    def test_solve_part_one(self):
        self.assertEqual(solve_part_one(self.data[0]), 33210)
        self.assertEqual(solve_part_one(self.data[1]), 490)
        self.assertEqual(solve_part_one(self.data[2]), 4243455)
        self.assertEqual(solve_part_one(self.data[3]), 401)

    def test_solve_part_two(self):
        self.assertEqual(solve_part_two(self.data[0]), 8544)
        self.assertEqual(solve_part_two(self.data[1]), 625)
        self.assertEqual(solve_part_two(self.data[2]), 3253600)
        self.assertEqual(solve_part_two(self.data[3]), 1058)

    def test_part_one(self):
        self.assertEqual(part1(self.data), 4277556)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 3263827)
