from unittest import TestCase

from aoc2022.d01 import last
from tools.file_loader import load_ints
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestCount(TestCase):
    def test_Sample(self):
        numbers = load_ints(get_test_file_path("samples/d01.txt"))
        self.assertEqual(last(numbers), 3)


