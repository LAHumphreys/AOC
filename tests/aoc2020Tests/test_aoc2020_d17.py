from unittest import TestCase
from aoc2020.d17 import load_initial_state, step_forward, get_neighbours, do_steps
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath

class Part1(TestCase):
    def test_initial_state(self):
        path = GetTestFilePath("samples/d17/sample1.txt")
        initial_state = load_initial_state(path)
        expected = {
            (0, 0, 1): 1,
            (0, 1, 2): 1,
            (0, 2, 0): 1,
            (0, 2, 1): 1,
            (0, 2, 2): 1,
        }
        self.assertDictEqual(expected, initial_state)

    def test_neighbours(self):
        expected = [
            (-1, -1, -1),
            (-1, -1, 0),
            (-1, -1, 1),

            (-1, 0, -1),
            (-1, 0, 0),
            (-1, 0, 1),

            (-1, 1, -1),
            (-1, 1, 0),
            (-1, 1, 1),

            (0, -1, -1),
            (0, -1, 0),
            (0, -1, 1),

            (0, 0, -1),
            (0, 0, 1),

            (0, 1, -1),
            (0, 1, 0),
            (0, 1, 1),

            (1, -1, -1),
            (1, -1, 0),
            (1, -1, 1),

            (1, 0, -1),
            (1, 0, 0),
            (1, 0, 1),

            (1, 1, -1),
            (1, 1, 0),
            (1, 1, 1),
        ]
        expected.sort()
        self.assertListEqual(expected, get_neighbours((0,0,0)))

    def test_step_forward(self):
        expected= {
            (-1, 1, 0): 1,
            (-1, 2, 2): 1,
            (-1, 3, 1): 1,

            (0, 1, 0): 1,
            (0, 1, 2): 1,
            (0, 2, 1): 1,
            (0, 2, 2): 1,
            (0, 3, 1): 1,

            (1, 1, 0): 1,
            (1, 2, 2): 1,
            (1, 3, 1): 1,
        }
        path = GetTestFilePath("samples/d17/sample1.txt")
        initial_state = load_initial_state(path)
        step_one = step_forward(initial_state)
        self.assertDictEqual(expected, step_one)
        self.assertEqual(11, len(step_one))

        step_two = step_forward(step_one)
        self.assertEqual(1 + 5 + 9 + 5 + 1, len(step_two))

    def test_do_steps(self):
        path = GetTestFilePath("samples/d17/sample1.txt")
        initial_state = load_initial_state(path)
        step_two = do_steps(initial_state, 2)
        self.assertEqual(21, len(step_two))

        step_six = do_steps(initial_state, 6)
        self.assertEqual(112, len(step_six))

class Part2(TestCase):
    def test_initial_state(self):
        path = GetTestFilePath("samples/d17/sample1.txt")
        initial_state = load_initial_state(path, dimensions=4)
        expected = {
            (0, 0, 0, 1): 1,
            (0, 0, 1, 2): 1,
            (0, 0, 2, 0): 1,
            (0, 0, 2, 1): 1,
            (0, 0, 2, 2): 1,
        }
        self.assertDictEqual(expected, initial_state)

    def test_do_steps(self):
        path = GetTestFilePath("samples/d17/sample1.txt")
        initial_state = load_initial_state(path, dimensions=4)
        step_six = do_steps(initial_state, 6, dimensions=4)
        self.assertEqual(848, len(step_six))

