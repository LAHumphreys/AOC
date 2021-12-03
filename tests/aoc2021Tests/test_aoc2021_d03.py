from unittest import TestCase

from aoc2021.d03 import calc_power_vars, calc_life_vars
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class TestCount(TestCase):
    def test_vars(self):
        lines = [l[:-1] for l in open(get_test_file_path("samples/d03.txt")).readlines()]
        vars = calc_power_vars(lines)
        self.assertEqual(vars.gamma, 22)
        self.assertEqual(vars.epsilon, 9)

    def test_o2(self):
        lines = [l[:-1] for l in open(get_test_file_path("samples/d03.txt")).readlines()]
        vars = calc_life_vars(lines)
        self.assertEqual(vars.o2, 23)
        self.assertEqual(vars.co2, 10)
