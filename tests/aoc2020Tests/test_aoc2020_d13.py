from unittest import TestCase

from aoc2020.d13 import time_to_wait, calc_part_one, load_notes, find_lcm, load_notes_with_offset, \
    find_common_departure_point
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class TimeToDestination(TestCase):
    def test_time_to_wait_start(self):
        self.assertEqual(0, time_to_wait(7, 0))
        self.assertEqual(6, time_to_wait(7, 939))

    def test_calc_answer(self):
        self.assertEqual(295, calc_part_one([7, 13, 59, 31, 19], 939))

    def test_notes(self):
        start_time, bus_ids = load_notes(GetTestFilePath("samples/d13/sample1.txt"))
        self.assertEqual(295, calc_part_one(bus_ids, start_time))


class TestCommon(TestCase):
    def test_lcm(self):
        self.assertEqual(91, find_lcm(7, 13))
        self.assertEqual(240, find_lcm(12, 80))

    def test_notes(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample1.txt"))
        expected = [(7, 0), (13, 1), (59, 4), (31, 6), (19, 7)]
        self.assertListEqual(expected, bus_ids)

    def test_example1(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample1.txt"))
        self.assertEqual(1068781, find_common_departure_point(bus_ids))

    def test_example2(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample2.txt"))
        self.assertEqual(3417, find_common_departure_point(bus_ids))

    def test_example3(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample3.txt"))
        self.assertEqual(754018, find_common_departure_point(bus_ids))

    def test_example4(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample4.txt"))
        self.assertEqual(779210, find_common_departure_point(bus_ids))

    def test_example5(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample5.txt"))
        self.assertEqual(1261476, find_common_departure_point(bus_ids))

    def test_example6(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/sample6.txt"))
        self.assertEqual(1202161486, find_common_departure_point(bus_ids))

    def test_actual(self):
        bus_ids = load_notes_with_offset(GetTestFilePath("samples/d13/actual_data.txt"))
        self.assertEqual(402251700208309, find_common_departure_point(bus_ids))
