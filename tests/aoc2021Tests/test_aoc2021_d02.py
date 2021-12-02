from unittest import TestCase

from aoc2021.d02 import calc_depth, calc_aim
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class TestCount(TestCase):
    def test_Sample(self):
        lines = open(get_test_file_path("samples/d02.txt")).readlines()
        self.assertEqual(calc_depth(lines), (15, 10))

    def test_aim(self):
        lines = open(get_test_file_path("samples/d02.txt")).readlines()
        self.assertEqual(calc_aim(lines), (15, 60))
