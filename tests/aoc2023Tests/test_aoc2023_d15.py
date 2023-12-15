from unittest import TestCase

from aoc2023.d14 import load_array, tilt_up, part_one, tilt_left
from aoc2023.d14 import do_cycle, do_cycles, count_top_weight, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestLoadArray(TestCase):
    def test_load(self):
        expected = [
            "O....#....",
            "O.OO#....#",
            ".....##...",
            "OO.#O....O",
            ".O.....O#.",
            "O.#..O.#.#",
            "..O..#O..O",
            ".......O..",
            "#....###..",
            "#OO..#...."
        ]
        self.assertListEqual(load_array(get_test_file_path("samples/d14.txt")), expected)
