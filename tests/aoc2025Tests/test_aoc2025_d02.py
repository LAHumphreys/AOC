from unittest import TestCase
from aoc2025.d02 import load_sample, get_next_repeat, get_invalid_ids, part1
from tests.aoc2025Tests.aoc2025_common import get_test_file_path

class TestDay02(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d02.txt")
        self.lines = load_sample(self.sample_path)

    def test_simple_next(self):
        self.assertEqual(get_next_repeat("10"), "11")
        self.assertEqual(get_next_repeat("11"), "22")
        self.assertEqual(get_next_repeat("95"), "99")
        self.assertEqual(get_next_repeat("998"), "1010")
        self.assertEqual(get_next_repeat("222220"), "222222")
        self.assertEqual(get_next_repeat("1188511880"), "1188511885")

    def test_invalid_ids(self):
        self.assertEqual(get_invalid_ids("11", "22"), [11, 22])
        self.assertEqual(get_invalid_ids("95", "115"), [99])
        self.assertEqual(get_invalid_ids("998", "1012"), [1010])
        self.assertEqual(get_invalid_ids("1188511880", "1188511890"), [1188511885])
    def test_part_one(self):
        self.assertEqual(part1(self.lines), 1227775554)
