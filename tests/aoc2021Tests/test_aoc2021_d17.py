from unittest import TestCase

from aoc2021.d17 import min_velocity_after,  find_all, Box
from aoc2021.d17 import run_simulation

class Runner(TestCase):
    def test_min_velocity(self):
        self.assertEqual(min_velocity_after(20), 6)
        self.assertEqual(min_velocity_after(9), 4)
        self.assertEqual(min_velocity_after(46), 10)
        self.assertEqual(min_velocity_after(30), 8)

    def test_run_vertical(self):
        min_x = 20
        max_x = 30
        min_y = -10
        max_y = -5
        self.assertEqual(True, run_simulation(6, 0, Box(min_x, max_x, min_y, max_y))[0])

    def test_run_all(self):
        min_x = 20
        max_x = 30
        min_y = -10
        max_y = -5
        matches = find_all(Box(min_x, max_x, min_y, max_y))
        self.assertEqual(len(matches), 112)
        self.assertEqual(True, run_simulation(6, 0, Box(min_x, max_x, min_y, max_y))[0])