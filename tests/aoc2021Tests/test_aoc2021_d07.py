from unittest import TestCase

from aoc2021.d07 import count_fuel, find_mid, part_one
from aoc2021.d07 import count_expo_steps, count_expo_fuel, part_two

class TestHorizontalMoving(TestCase):
    def test_map_state(self):
        self.assertEqual(count_fuel(1,  [16,1,2,0,4,2,7,1,2,14]), 41)
        self.assertEqual(count_fuel(2,  [16,1,2,0,4,2,7,1,2,14]), 37)
        self.assertEqual(count_fuel(3,  [16,1,2,0,4,2,7,1,2,14]), 39)
        self.assertEqual(count_fuel(10, [16,1,2,0,4,2,7,1,2,14]), 71)

    def test_find_mid(self):
        self.assertEqual(find_mid([16,1,2,0,4,2,7,1,2,14]), 2)

    def test_part_one(self):
        self.assertEqual(part_one([16,1,2,0,4,2,7,1,2,14]), 37)

    def test_expo_steps(self):
        self.assertEqual(count_expo_steps(4, 5), 1)
        self.assertEqual(count_expo_steps(7, 5), 3)
        self.assertEqual(count_expo_steps(2, 5), 6)
        self.assertEqual(count_expo_steps(1, 5), 10)
        self.assertEqual(count_expo_steps(0, 5), 15)
        self.assertEqual(count_expo_steps(14, 5), 45)
        self.assertEqual(count_expo_steps(16, 5), 66)

    def test_expo_fuel(self):
        self.assertEqual(count_expo_fuel(5,  [16,1,2,0,4,2,7,1,2,14]), 168)
        self.assertEqual(count_expo_fuel(2,  [16,1,2,0,4,2,7,1,2,14]), 206)

    def test_part_two(self):
        self.assertEqual(part_two([16,1,2,0,4,2,7,1,2,14]), 168)
