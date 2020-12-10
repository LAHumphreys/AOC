from aoc2020.d10 import part_1, part_2
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath
from unittest import TestCase


class TestPart1(TestCase):
    def test_example1(self):
        path = GetTestFilePath("samples/d10/example1")
        self.assertEqual(part_1(path), 35)

    def test_example2(self):
        path = GetTestFilePath("samples/d10/example2")
        self.assertEqual(part_1(path), 220)


class TestPart2(TestCase):
    def test_example1(self):
        path = GetTestFilePath("samples/d10/example1")
        self.assertEqual(part_2(path), 8)

    def test_example2(self):
        path = GetTestFilePath("samples/d10/example2")
        self.assertEqual(part_2(path), 19208)
