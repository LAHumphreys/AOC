from unittest import TestCase

from aoc2022.d01 import load_elves, get_elves_with_most, Elf
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestCount(TestCase):
    def test_Load(self):
        elves = load_elves(get_test_file_path("samples/d01.txt"))
        self.assertListEqual(elves[0].carrying, [1000, 2000, 3000])
        self.assertEqual(elves[0].total, 6000)

    def test_Sample(self):
        elves = load_elves(get_test_file_path("samples/d01.txt"))
        self.assertEqual(len(elves), 5)
        elves = get_elves_with_most(elves, 1)
        self.assertListEqual([Elf(carrying=[7000, 8000, 9000], total=24000)], elves)

    def test_Sample_Part2(self):
        elves = load_elves(get_test_file_path("samples/d01.txt"))
        self.assertEqual(len(elves), 5)
        elves = get_elves_with_most(elves, 3)
        self.assertListEqual([Elf(carrying=[10000], total=10000),
                              Elf(carrying=[5000, 6000], total=11000),
                              Elf(carrying=[7000, 8000, 9000], total=24000),
                              ], elves)
