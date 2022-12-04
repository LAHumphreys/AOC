from unittest import TestCase

from aoc2022.d04 import Elf, load_pairs, count_overlap, count_partial_overlap
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestLoad(TestCase):
    def setUp(self) -> None:
        self.pairs = [
            (Elf(min=2, max=4), Elf(min=6, max=8)),
            (Elf(min=2, max=3), Elf(min=4, max=5)),
            (Elf(min=5, max=7), Elf(min=7, max=9)),
            (Elf(min=2, max=8), Elf(min=3, max=7)),
            (Elf(min=6, max=6), Elf(min=4, max=6)),
            (Elf(min=2, max=6), Elf(min=4, max=8))
        ]

    def test_load_all_lines(self):
        elves = load_pairs(get_test_file_path("samples/d04.txt"))
        self.assertListEqual(elves, self.pairs)


class TestPart1(TestCase):
    def test_sample(self):
        elves = load_pairs(get_test_file_path("samples/d04.txt"))
        self.assertEqual(count_overlap(elves), 2)


class TestPart2(TestCase):
    def test_sample(self):
        elves = load_pairs(get_test_file_path("samples/d04.txt"))
        self.assertEqual(count_partial_overlap(elves), 4)
