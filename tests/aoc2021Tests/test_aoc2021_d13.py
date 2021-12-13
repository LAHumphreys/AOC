from unittest import TestCase

from aoc2021.d13 import fold_fixed_y, fold_fixed_x, fold_grid, load_grid, load_folds, part_one
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class CorruptDetector(TestCase):

    def test_fold_y(self):
        self.assertEqual(fold_fixed_y((0, 0), 7), (0, 0))
        self.assertEqual(fold_fixed_y((2, 0), 7), (2, 0))
        self.assertEqual(fold_fixed_y((0, 14), 7), (0, 0))
        self.assertEqual(fold_fixed_y((2, 14), 7), (2, 0))

    def test_fold_x(self):
        self.assertEqual(fold_fixed_x((0, 0), 7), (0, 0))
        self.assertEqual(fold_fixed_x((0, 2), 7), (0, 2))
        self.assertEqual(fold_fixed_x((14, 0), 7), (0, 0))
        self.assertEqual(fold_fixed_x((14, 2), 7), (0, 2))

    def test_fold_x_grid(self):
        grid = {
            (0, 0): 1,
            (0, 2): 1,
            (14, 0): 1,
            (14, 2): 1,
        }
        new_grid = {
            (0, 0): 2,
            (0, 2): 2,
        }
        self.assertDictEqual(fold_grid(grid, (7, None)), new_grid)

    def test_load_grid(self):
        grid = load_grid(get_test_file_path("samples/d13/grid.txt"))
        self.assertEqual(len(grid), 18)
        self.assertEqual(grid[(6,10)], 1)
        self.assertEqual(grid[(9,0)], 1)
        self.assertEqual(grid[(10,12)], 1)

    def test_load_folds(self):
        folds = load_folds(get_test_file_path("samples/d13/folds.txt"))
        self.assertListEqual(folds, [(None, 7), (5, None)])

    def test_part_one(self):
        grid = load_grid(get_test_file_path("samples/d13/grid.txt"))
        folds = load_folds(get_test_file_path("samples/d13/folds.txt"))
        self.assertEqual(part_one(grid, folds[0:1]), 17)

