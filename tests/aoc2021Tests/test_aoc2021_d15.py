from unittest import TestCase

from aoc2021.d15 import calc_cost_map, load_map, enlarge_map
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class CostCalculator(TestCase):
    def test_tiny_cost_map(self):
        map = [
            [2, 1],
            [8, 1],
        ]

        cost_map = [
            [2, 1],
            [1, 0],
        ]

        result = calc_cost_map(map, (1, 1))
        self.assertListEqual(cost_map, result)


    def test_small_cost_map(self):
        map = [
            [6, 3, 9],
            [5, 2, 1],
            [5, 9, 1],
        ]

        cost_map = [
            [7, 4, 2],
            [4, 2, 1],
            [9, 1, 0],
        ]

        result = calc_cost_map(map)
        self.assertListEqual(cost_map, result)

    def test_load(self):
        loaded = load_map(get_test_file_path("samples/d15/small.txt"))
        map = [
            [6, 3, 9],
            [5, 2, 1],
            [5, 9, 1],
        ]
        self.assertListEqual(loaded, map)

    def test_sample(self):
        map = load_map(get_test_file_path("samples/d15/sample.txt"))
        cost_map = calc_cost_map(map)
        self.assertEqual(cost_map[0][0], 40)

    def test_tiny_enlarge(self):
        cave_map = [
            [2, 1],
            [8, 1],
        ]
        enlarged = [
            [2, 1, 3, 2],
            [8, 1, 9, 2],
            [3, 2, 4, 3],
            [9, 2, 1, 3],
        ]
        calculated_map = enlarge_map(2, cave_map)
        self.assertListEqual(calculated_map, enlarged)

    def test_unit_enlarge(self):
        cave_map = [
            [8]
        ]
        enlarged = [
            [8,9,1,2,3],
            [9,1,2,3,4],
            [1,2,3,4,5],
            [2,3,4,5,6],
            [3,4,5,6,7],
        ]
        calculated_map = enlarge_map(5, cave_map)
        self.assertListEqual(calculated_map, enlarged)

    def test_enlarge(self):
        cave_map = load_map(get_test_file_path("samples/d15/sample.txt"))
        enlarged_cave_map = load_map(get_test_file_path("samples/d15/large_sample.txt"))
        calculated_map = enlarge_map(5, cave_map)
        self.assertListEqual(calculated_map, enlarged_cave_map)


    def test_enlarged_sample(self):
        cave_map = load_map(get_test_file_path("samples/d15/sample.txt"))
        enlarged_map = enlarge_map(5, cave_map)
        cost_map = calc_cost_map(enlarged_map)
        self.assertEqual(cost_map[0][0], 315)
