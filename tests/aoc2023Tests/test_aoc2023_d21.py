from unittest import TestCase

from aoc2023.d21 import load_garden, apply_step, apply_steps, count_options
from aoc2023.d21 import expand_garden
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestFlipFlop(TestCase):
    def test_initial_step(self):
        initial = load_garden(get_test_file_path("samples/d21/input.txt"))
        expected = load_garden(get_test_file_path("samples/d21/first.txt"))
        self.assertEqual(apply_step(initial).plots, expected.plots)

    def test_two_steps(self):
        initial = load_garden(get_test_file_path("samples/d21/input.txt"))
        expected = load_garden(get_test_file_path("samples/d21/second.txt"))
        self.assertEqual(apply_steps(initial, 2).plots, expected.plots)

    def test_three_steps(self):
        initial = load_garden(get_test_file_path("samples/d21/input.txt"))
        expected = load_garden(get_test_file_path("samples/d21/three.txt"))
        self.assertEqual(apply_steps(initial, 3).plots, expected.plots)

    def test_six_steps(self):
        initial = load_garden(get_test_file_path("samples/d21/input.txt"))
        expected = load_garden(get_test_file_path("samples/d21/six.txt"))
        options = apply_steps(initial, 6)
        self.assertEqual(options.plots, expected.plots)
        self.assertEqual(count_options(options), 16)


class TestExpand(TestCase):
    def test_six_steps(self):
        initial = load_garden(get_test_file_path("samples/d21/input.txt"))
        expanded = expand_garden(initial)
        apply_steps(expanded, 18)
