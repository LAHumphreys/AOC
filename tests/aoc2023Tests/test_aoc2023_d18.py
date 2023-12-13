from unittest import TestCase

from aoc2023.d18 import load_instructions, Direction, get_bounds, draw_trench
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestLoad(TestCase):
    def test_directions(self):
        instructions = load_instructions(get_test_file_path("samples/d18.txt"))
        self.assertEqual(instructions[0].direction, Direction(x=6, y=0))
        self.assertEqual(instructions[1].direction, Direction(x=0, y=5))
        self.assertEqual(instructions[2].direction, Direction(x=-2, y=0))
        self.assertEqual(instructions[-1].direction, Direction(y=-2, x=0))

    def test_bounds(self):
        instructions = load_instructions(get_test_file_path("samples/d18.txt"))
        self.assertEqual(get_bounds(instructions), (8, 11, 1, 1))
        draw_trench(instructions)
