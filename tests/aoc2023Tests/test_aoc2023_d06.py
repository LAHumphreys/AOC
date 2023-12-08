from unittest import TestCase

from aoc2023.d06 import calculate_times, load_races, Race, part_one
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_example_one(self):
        self.assertEqual(calculate_times(7, 9), 4)

    def test_example_two(self):
        self.assertEqual(calculate_times(15, 40), 8)

    def test_load(self):
        races = load_races(get_test_file_path("samples/d06.txt"))
        expected = [Race(race_time=7, max_distance=9),
                    Race(race_time=15, max_distance=40),
                    Race(race_time=30, max_distance=200)]
        self.assertListEqual(races, expected)

    def test_part_one(self):
        races = load_races(get_test_file_path("samples/d06.txt"))
        self.assertEqual(part_one(races), 288)

    def test_part_two(self):
        self.assertEqual(calculate_times(race_time=71530, record_distance=940200), 71503)
