from unittest import TestCase

from aoc2023.d09 import get_diffs, get_series_calculator, apply_polynomial, get_item
from aoc2023.d09 import load_series, part_one, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestNext(TestCase):
    def test_diffs_single(self):
        self.assertListEqual(get_diffs([0, 3, 6, 9, 12, 15]), [3, 3, 3, 3, 3])
        self.assertListEqual(get_diffs([1, 3, 6, 10, 15, 21]), [2, 3, 4, 5, 6])

    def test_calculator_simple_diff(self):
        series = [0, 3, 6, 9, 12, 15]
        poly = get_series_calculator(series)
        print(poly)
        regen = [apply_polynomial(n, poly) for n in range(1, 7)]
        self.assertListEqual(series, regen)

    def test_calculator(self):
        series = [1, 3, 6, 10, 15, 21]
        poly = get_series_calculator(series)
        regen = [apply_polynomial(n, poly) for n in range(1, 7)]
        self.assertListEqual(series, regen)

    def test_calculator_cubes(self):
        series = [10, 13, 16, 21, 30, 45]
        poly = get_series_calculator(series)
        print(poly)
        regen = [round(apply_polynomial(n, poly),7) for n in range(1, 7)]
        self.assertListEqual(series, regen)

    def test_calculator_real(self):
        series = [10, 9, 7, 18, 72, 228, 601, 1407, 3030, 6115, 11691, 21328, 37332, 62982, 102813, 162949, 251490, 378957, 558799, 807966, 1147552]
        poly = get_series_calculator(series)
        regen = [round(apply_polynomial(n, poly)) for n in range(1, len(series) +1)]
        self.assertListEqual(series, regen)

    def test_calculator_real_2(self):
        series = [15, 24, 45, 84, 160, 333, 746, 1690, 3708, 7756, 15432, 29276, 53164, 92931, 157702, 263310, 441377, 762715, 1394801, 2735901, 5712640]
        poly = get_series_calculator(series)
        print (poly)
        regen = [round(apply_polynomial(n, poly)) for n in range(1, len(series) +1)]
        self.assertListEqual(series, regen)

    def test_next(self):
        self.assertEqual(get_item([0, 3, 6, 9, 12, 15]), 18)
        self.assertEqual(get_item([1, 3, 6, 10, 15, 21]), 28)
        self.assertEqual(get_item([10, 13, 16, 21, 30, 45]), 68)

    def test_part_one(self):
        all_series = load_series(get_test_file_path("samples/d09.txt"))
        self.assertEqual(part_one(all_series), 114)

    def test_part_two(self):
        all_series = load_series(get_test_file_path("samples/d09.txt"))
        self.assertEqual(part_two(all_series), 2)


