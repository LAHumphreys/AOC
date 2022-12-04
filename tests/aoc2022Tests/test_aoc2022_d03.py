from unittest import TestCase

from aoc2022.d03 import score, load_rucksacks, RuckSack, get_repeat
from aoc2022.d03 import get_badge, get_groups
from tests.aoc2022Tests.aoc2022_common import get_test_file_path


class TestScore(TestCase):
    def test_lower(self):
        self.assertEqual(score("a"), 1)
        self.assertEqual(score("z"), 26)

    def test_upper(self):
        self.assertEqual(score("A"), 27)
        self.assertEqual(score("Z"), 52)


class TestLoad(TestCase):
    def setUp(self) -> None:
        self.all_items = [score(x) for x in "cfghhpprrstvwwFFFFJJMMWW"]

        self.first_pockets = ([x for x in "gprrtvwwJJWW"],
                              [x for x in "cfhhpsFFFFMM"])

        self.first_scored_pockets = ([score(x) for x in self.first_pockets[0]],
                                     [score(x) for x in self.first_pockets[1]])

        self.first_scored_pockets = ([score(x) for x in self.first_pockets[0]],
                                     [score(x) for x in self.first_pockets[1]])

    def test_load_all_lines(self):
        rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))
        self.assertEqual(len(rucksacks), 6)

    def test_load_split_in_two(self):
        rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))
        self.assertListEqual(self.first_scored_pockets[0], rucksacks[0].first)
        self.assertListEqual(self.first_scored_pockets[1], rucksacks[0].last)

    def test_load_all_items(self):
        rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))
        self.assertListEqual(self.all_items, rucksacks[0].all_items)


class TestRepeat(TestCase):
    def setUp(self) -> None:
        self.rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))

    def test_first(self):
        self.assertEqual(get_repeat(self.rucksacks[0]), 16)


class TestBadge(TestCase):
    def test_first(self):
        packs = (RuckSack(all_items=[0,2,3], first=[], last=[]),
                 RuckSack(all_items=[0,5,6], first=[], last=[]),
                 RuckSack(all_items=[0,435345,8], first=[], last=[]))
        self.assertEqual(get_badge(packs), 0)

    def test_mixed(self):
        packs = (RuckSack(all_items=[1,2,7], first=[], last=[]),
                 RuckSack(all_items=[3,5,6,7,8], first=[], last=[]),
                 RuckSack(all_items=[7,435345,8], first=[], last=[]))
        self.assertEqual(get_badge(packs), 7)


class TestGroups(TestCase):
    def test_get(self):
        rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))
        groups = get_groups(rucksacks)
        self.assertEqual(len(groups), 2)

    def test_get_group_badge(self):
        rucksacks = load_rucksacks(get_test_file_path("samples/d03.txt"))
        groups = get_groups(rucksacks)
        self.assertEqual(get_badge(groups[0]), 18)
        self.assertEqual(get_badge(groups[1]), 52)
