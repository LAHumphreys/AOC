from unittest import TestCase
from aoc2025.d04 import load_sample, part1, count_row, count_rows
from aoc2025.d04 import  part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay04(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d04.txt")
        # Ensure the sample file exists even if empty for load_sample
        self.data = load_sample(self.sample_path)

    def test_count_row(self):
        self.assertEqual(count_row("..@@.@@@@."), [0, 1, 2, 2, 2, 2, 3, 3, 2, 1])

    def test_count_rolls(self   ):
        counted = count_rows(self.data)
        self.assertEqual(counted[0], [0, 0, 4, 4, 0, 4, 4, 5, 4, 0])


    def test_part_one(self):
        self.assertEqual(part1(self.data), 13)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 43)
