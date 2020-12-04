from aoc2020.d03 import Map, countTrees
from unittest import TestCase

class Test_Map(TestCase):
    def test_simpleMap(self):
        code = [
            "12",
            "ab",
            "AB"
        ]
        map = Map(code)
        self.assertEqual(map.GetCoord(0,0), "1")
        self.assertEqual(map.GetCoord(1,1), "b")

    def test_simpleMap_NotSquare(self):
        code = [
            "1234",
            "abcd",
            "ABCD"
        ]
        map = Map(code)
        self.assertEqual(map.GetCoord(3,1), "d")
        self.assertEqual(map.GetCoord(11,2), "D")
        self.assertEqual(map.GetHeight(), 3)


    def test_simpleMapWrapX(self):
        code = [
            "12",
            "ab",
            "AB"
        ]
        map = Map(code)
        self.assertEqual(map.GetCoord(2,2), "A")

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
        self.assertEqual(7, countTrees(coords, 3, 1))
        self.assertEqual(2, countTrees(coords, 1, 1))
        self.assertEqual(3, countTrees(coords, 5, 1))
        self.assertEqual(4, countTrees(coords, 7, 1))
        self.assertEqual(2, countTrees(coords, 1, 2))
