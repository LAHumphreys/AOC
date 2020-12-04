from unittest import TestCase

from aoc2019.d01 import calc_fuel, calc_total_fuel, calc_rocket_fuel, total_rocket_fuel


class TestCalcFuel(TestCase):
    def test_fuel_examples(self):
        self.assertEqual(calc_fuel(12), 2)
        self.assertEqual(calc_fuel(14), 2)
        self.assertEqual(calc_fuel(1969), 654)
        self.assertEqual(calc_fuel(100756), 33583)

    def test_fuel_cornerCases_tooSmal(self):
        self.assertEqual(calc_fuel(3), 0)

    def test_totalFueld(self):
        self.assertEqual(calc_total_fuel([12, 14, 1969]), 2 + 2 + 654)


class TestCalcRocketFuel(TestCase):
    def test_fuel_examples(self):
        self.assertEqual(calc_rocket_fuel(14), 2)
        self.assertEqual(calc_rocket_fuel(1969), 966)
        self.assertEqual(calc_rocket_fuel(100756), 50346)

    def test_totalFueld(self):
        self.assertEqual(total_rocket_fuel([14, 1969, 100756]), 2 + 966 + 50346)
