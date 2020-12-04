from unittest import TestCase

from aoc2020.d03 import Map, count_trees


class Test_Map(TestCase):
    def test_simpleMap(self):
        code = [
            "12",
            "ab",
            "AB"
        ]
        map = Map(code)
        self.assertEqual(map.get_coord(0, 0), "1")
        self.assertEqual(map.get_coord(1, 1), "b")

    def test_simpleMap_NotSquare(self):
        code = [
            "1234",
            "abcd",
            "ABCD"
        ]
        map = Map(code)
        self.assertEqual(map.get_coord(3, 1), "d")
        self.assertEqual(map.get_coord(11, 2), "D")
        self.assertEqual(map.get_height(), 3)

    def test_simpleMapWrapX(self):
        code = [
            "12",
            "ab",
            "AB"
        ]
        map = Map(code)
        self.assertEqual(map.get_coord(2, 2), "A")


class TestTreeCount(TestCase):
    def test_example1(self):
        coords = [
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#",
        ]
        self.assertEqual(7, count_trees(coords, 3, 1))
        self.assertEqual(2, count_trees(coords, 1, 1))
        self.assertEqual(3, count_trees(coords, 5, 1))
        self.assertEqual(4, count_trees(coords, 7, 1))
        self.assertEqual(2, count_trees(coords, 1, 2))
