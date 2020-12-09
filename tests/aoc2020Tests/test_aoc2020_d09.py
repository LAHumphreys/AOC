from unittest import TestCase
from tools.file_loader import load_ints

from tests.aoc2020Tests.aoc2020_common import GetTestFilePath
from aoc2020.d09 import part_two, part_one, is_valid


class TestPart1(TestCase):
    def test_Example1(self):
        path = GetTestFilePath("samples/d09/example1")
        values = load_ints(path)
        self.assertEqual(part_one(values, 5), 127)


class TestPart2(TestCase):
    def test_Example2(self):
        path = GetTestFilePath("samples/d09/example1")
        values = load_ints(path)
        self.assertEqual(part_two(values, 127), 62)

