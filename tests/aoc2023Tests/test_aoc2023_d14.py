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

    def test_tilt_up(self):
        expected = [
            "OOOO.#.O..",
            "OO..#....#",
            "OO..O##..O",
            "O..#.OO...",
            "........#.",
            "..#....#.#",
            "..O..#.O.O",
            "..O.......",
            "#....###..",
            "#....#...."
        ]
        array = load_array(get_test_file_path("samples/d14.txt"))
        self.assertListEqual(tilt_up(array), expected)

    def test_tilt_left(self):
        input = [
            "OOOO.#.O..",
            "OO..#....#",
            "OO..O##..O",
            "O..#.OO...",
            "........#.",
            "..#....#.#",
            "..O..#.O.O",
            "..O.......",
            "#....###..",
            "#....#...."
        ]
        expected = [
            "OOOO.#O...",
            "OO..#....#",
            "OOO..##O..",
            "O..#OO....",
            "........#.",
            "..#....#.#",
            "O....#OO..",
            "O.........",
            "#....###..",
            "#....#...."
        ]
        self.assertListEqual(tilt_left(input), expected)

    def test_part_one(self):
        array = load_array(get_test_file_path("samples/d14.txt"))
        self.assertEqual(part_one(array), 136)

    def test_cycle_one_turn(self):
        expected = [
            ".....#....",
            "....#...O#",
            "...OO##...",
            ".OO#......",
            ".....OOO#.",
            ".O#...O#.#",
            "....O#....",
            "......OOOO",
            "#...O###..",
            "#..OO#...."
        ]
        array = load_array(get_test_file_path("samples/d14.txt"))
        self.assertListEqual(do_cycle(array), expected)

    def test_cycle_two_turns(self):
            expected = [
                ".....#....",
                "....#...O#",
                ".....##...",
                "..O#......",
                ".....OOO#.",
                ".O#...O#.#",
                "....O#...O",
                ".......OOO",
                "#..OO###..",
                "#.OOO#...O"
            ]

            array = load_array(get_test_file_path("samples/d14.txt"))
            self.assertListEqual(do_cycles(array, 2), expected)

    def test_cycle_three_turns(self):
        expected = [
            ".....#....",
            "....#...O#",
            ".....##...",
            "..O#......",
            ".....OOO#.",
            ".O#...O#.#",
            "....O#...O",
            ".......OOO",
            "#...O###.O",
            "#.OOO#...O"
        ]

        array = load_array(get_test_file_path("samples/d14.txt"))
        self.assertListEqual(do_cycles(array, 3), expected)

    def test_cycle_1B_turns(self):
        array = load_array(get_test_file_path("samples/d14.txt"))
        cycled_array = do_cycles(array, 1000000000)
        self.assertEqual(count_top_weight(cycled_array), 64)

    def test_part_two(self):
        array = load_array(get_test_file_path("samples/d14.txt"))
        self.assertEqual(part_two(array), 64)
