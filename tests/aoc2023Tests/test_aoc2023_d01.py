from unittest import TestCase

from aoc2023.d01 import calculate_calibration, load_calibration, calculate_calibration2, find_numeric
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_calibrate(self):
        lines = load_calibration(get_test_file_path("samples/d01.txt"))
        self.assertEqual(calculate_calibration(lines), 142)

    def test_numeric(self):
        self.assertEqual(find_numeric("two1nine"), 29)
        self.assertEqual(find_numeric("eightwothree"), 83)
        self.assertEqual(find_numeric("abcone2threexyz"), 13)
        self.assertEqual(find_numeric("xtwone3four"), 24)
        self.assertEqual(find_numeric("4nineeightseven2"), 42)
        self.assertEqual(find_numeric("zoneight234"), 14)
        self.assertEqual(find_numeric("7pqrstsixteen"), 76)
        self.assertEqual(find_numeric("cpxtthree14"), 34)

    def test_calibrate2(self):
        lines = load_calibration(get_test_file_path("samples/d01_part2.txt"))
        self.assertEqual(calculate_calibration2(lines), 281)
