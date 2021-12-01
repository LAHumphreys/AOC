from unittest import TestCase

from aoc2021.d01 import count_increases, count_trios
from tools.file_loader import load_ints
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class TestCount(TestCase):
    def test_Sample(self):
        numbers = load_ints(get_test_file_path("samples/d01.txt"))
        self.assertEqual(count_increases(numbers), 7)


class TestWindow(TestCase):
    def test_Sample(self):
        numbers = load_ints(get_test_file_path("samples/d01.txt"))
        self.assertEqual(count_trios(numbers), 5)
