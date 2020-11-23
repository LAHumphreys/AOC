from unittest import TestCase
from aoc2019.d01 import CalcFuel, TotalFuel, CalcRocketFuel, TotalRocketFuel


class TestCalcFuel(TestCase):
    def test_fuel_examples(self):
        self.assertEqual(CalcFuel(12), 2)
        self.assertEqual(CalcFuel(14), 2)
        self.assertEqual(CalcFuel(1969), 654)
        self.assertEqual(CalcFuel(100756), 33583)

    def test_fuel_cornerCases_tooSmal(self):
        self.assertEqual(CalcFuel(3), 0)

    def test_totalFueld(self):
        self.assertEqual(TotalFuel([12, 14, 1969]), 2 + 2 + 654)

class TestCalcRocketFuel(TestCase):
    def test_fuel_examples(self):
        self.assertEqual(CalcRocketFuel(14), 2)
        self.assertEqual(CalcRocketFuel(1969), 966)
        self.assertEqual(CalcRocketFuel(100756), 50346)

    def test_totalFueld(self):
        self.assertEqual(TotalRocketFuel([14, 1969, 100756]), 2 + 966 + 50346)
