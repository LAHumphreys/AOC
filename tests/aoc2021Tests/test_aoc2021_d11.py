from unittest import TestCase

from aoc2021.d11 import do_step, load_tentacle, do_steps
from aoc2021.d11 import find_simultaneous_flash
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class CorruptDetector(TestCase):
    def test_increment(self):
        tentacle = [
            [1, 1, 1, 1, 1],
            [1, 8, 8, 8, 1],
            [1, 8, 1, 8, 1],
            [1, 8, 8, 8, 1],
            [1, 1, 1, 1, 1]
        ]
        result = [
            [2, 2, 2, 2, 2],
            [2, 9, 9, 9, 2],
            [2, 9, 2, 9, 2],
            [2, 9, 9, 9, 2],
            [2, 2, 2, 2, 2]
        ]
        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, result)
        self.assertEqual(flashed, 0)

    def test_sample_itter(self):
        tentacle = [
            [1, 1, 1, 1, 1],
            [1, 9, 9, 9, 1],
            [1, 9, 1, 9, 1],
            [1, 9, 9, 9, 1],
            [1, 1, 1, 1, 1]
        ]

        result = [
            [3, 4, 5, 4, 3],
            [4, 0, 0, 0, 4],
            [5, 0, 0, 0, 5],
            [4, 0, 0, 0, 4],
            [3, 4, 5, 4, 3]
        ]
        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, result)
        self.assertEqual(flashed, 9)

    def test_small_board_sample(self):
        tentacle = load_tentacle(get_test_file_path("samples/d11/small_board/initial_state.txt"))
        step_1 = load_tentacle(get_test_file_path("samples/d11/small_board/step_1.txt"))
        step_2 = load_tentacle(get_test_file_path("samples/d11/small_board/step_2.txt"))

        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, step_1)
        self.assertEqual(flashed, 9)

        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, step_2)
        self.assertEqual(flashed, 0)

    def test_large_board_sample_steps(self):
        tentacle = load_tentacle(get_test_file_path("samples/d11/large_board/initial_state.txt"))
        step_1 = load_tentacle(get_test_file_path("samples/d11/large_board/step_1.txt"))
        step_2 = load_tentacle(get_test_file_path("samples/d11/large_board/step_2.txt"))

        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, step_1)

        flashed = do_step(tentacle)
        self.assertListEqual(tentacle, step_2)

    def test_large_board_sample_10(self):
        tentacle = load_tentacle(get_test_file_path("samples/d11/large_board/initial_state.txt"))
        step_10 = load_tentacle(get_test_file_path("samples/d11/large_board/step_10.txt"))

        flashed = do_steps(tentacle, 10)
        self.assertListEqual(tentacle, step_10)
        self.assertEqual(flashed, 204)

    def test_large_board_sample_100(self):
        tentacle = load_tentacle(get_test_file_path("samples/d11/large_board/initial_state.txt"))
        step_100 = load_tentacle(get_test_file_path("samples/d11/large_board/step_100.txt"))

        flashed = do_steps(tentacle, 100)
        self.assertListEqual(tentacle, step_100)
        self.assertEqual(flashed, 1656)

    def test_simultaneous_flash(self):
        tentacle = load_tentacle(get_test_file_path("samples/d11/large_board/initial_state.txt"))
        self.assertEqual(find_simultaneous_flash(tentacle), 195)
