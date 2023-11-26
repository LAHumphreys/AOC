from unittest import TestCase

from aoc2023.d01 import load_elves
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_Load(self):
        elves = load_elves(get_test_file_path("samples/d01.txt"))
        self.assertListEqual(elves[0].carrying, [1000, 2000, 3000])
        self.assertEqual(elves[0].total, 6000)

