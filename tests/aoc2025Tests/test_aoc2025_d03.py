from unittest import TestCase
from aoc2025.d03 import load_sample, part1, max_joltage_from_bank
from aoc2025.d03 import unsafe_joltage_from_bank, part2
from tests.aoc2025Tests.aoc2025_common import get_test_file_path


class TestDay03(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d03.txt")
        self.data = load_sample(self.sample_path)

    def test_max_joltage_from_bank(self):
        self.assertEqual(max_joltage_from_bank("987654321111111"),  98)
        self.assertEqual(max_joltage_from_bank("811111111111119"), 89)
        self.assertEqual(max_joltage_from_bank("234234234234278"), 78)
        self.assertEqual(max_joltage_from_bank("818181911112111"), 92)

    def test_unsafe_joltage_from_bank(self):
        self.assertEqual(unsafe_joltage_from_bank("987654321111111"),  987654321111)
        self.assertEqual(unsafe_joltage_from_bank("811111111111119"), 811111111119)
        self.assertEqual(unsafe_joltage_from_bank("234234234234278"), 434234234278)
        self.assertEqual(unsafe_joltage_from_bank("818181911112111"), 888911112111)

    def test_part_one(self):
        self.assertEqual(part1(self.data), 357)

    def test_part_two(self):
        self.assertEqual(part2(self.data), 3121910778619)
