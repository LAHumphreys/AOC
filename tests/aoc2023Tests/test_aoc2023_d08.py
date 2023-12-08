from unittest import TestCase

from aoc2023.d08 import load_map, part_one, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestLoad(TestCase):
    def test_sample(self):
        map = load_map(get_test_file_path("samples/d08.txt"))
        self.assertEqual(map.directions, "LLR")
        self.assertEqual(map.nodes["AAA"].left, "BBB")
        self.assertEqual(map.nodes["AAA"].right, "BBB")

    def test_part_one(self):
        map = load_map(get_test_file_path("samples/d08.txt"))
        self.assertEqual(part_one(map), 6)

    def test_part_two(self):
        map = load_map(get_test_file_path("samples/d08_part2.txt"))
        self.assertEqual(part_two(map), 6)
