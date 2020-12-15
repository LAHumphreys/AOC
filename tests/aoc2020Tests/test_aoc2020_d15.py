from unittest import TestCase

from aoc2020.d15 import part_one
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class PartOne(TestCase):
    def test_part_one(self):
        path = GetTestFilePath("samples/d15/sample1.txt")
        self.assertEqual("hello", part_one(path))

    def test_part_two(self):
        path = GetTestFilePath("samples/d15/sample2.txt")
        self.assertEqual("world", part_one(path))
