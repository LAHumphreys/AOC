from unittest import TestCase

from aoc2021.d09 import load_data_rows, find_minimums, LocalMinimum, part_one
from aoc2021.d09 import get_basin_size, part_two
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class SignalSets(TestCase):
    def test_load_data(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        expected = [
            [2,1,9,9,9,4,3,2,1,0],
            [3,9,8,7,8,9,4,9,2,1],
            [9,8,5,6,7,8,9,8,9,2],
            [8,7,6,7,8,9,6,7,8,9],
            [9,8,9,9,9,6,5,6,7,8]
        ]
        self.assertListEqual(data, expected)

    def test_basin_sample_one(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(3, get_basin_size(data, 1, 0))

    def test_basin_sample_top_right(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(9, get_basin_size(data, 9, 0))

    def test_basin_sample_middle(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(14, get_basin_size(data, 2, 2))

    def test_basin_bottom_right(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(9, get_basin_size(data, 6, 4))


    def test_part_one(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(part_one(data), 15)

    def test_part_two(self):
        data = load_data_rows(get_test_file_path("samples/d09.txt"))
        self.assertEqual(part_two(data), 1134)

    def test_find_minimums(self):
        minimums = find_minimums(load_data_rows(get_test_file_path("samples/d09.txt")))
        self.assertEqual(len(minimums), 4)
        self.assertEqual(minimums[0], LocalMinimum(x=1, y=0, value=1))
        self.assertEqual(minimums[1], LocalMinimum(x=2, y=2, value=5))
        self.assertEqual(minimums[2], LocalMinimum(x=6, y=4, value=5))
        self.assertEqual(minimums[3], LocalMinimum(x=9, y=0, value=0))

    def test_find_minimums_centre(self):
        control = [
            [9,9,9],
            [9,5,9],
            [9,9,9]
        ]
        minimums = find_minimums(control)
        self.assertEqual(len(minimums), 1)





