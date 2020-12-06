from unittest import TestCase

from aoc2020.d06 import match_group, merge_group


class Test_Part1(TestCase):
    def test_merge(self):
        groups = [
            ["abc"],
            ["a", "b", "c"],
            ["ab", "ac"],
            ["a", "a", "a", "a"],
            ["b"]
        ]
        self.assertEqual(11, merge_group(groups))


class Test_Part2(TestCase):
    def test_match(self):
        groups = [
            ["abc"],
            ["a", "b", "c"],
            ["ab", "ac"],
            ["a", "a", "a", "a"],
            ["b"]
        ]
        self.assertEqual(6, match_group(groups))
