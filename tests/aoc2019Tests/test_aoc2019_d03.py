from unittest import TestCase
from aoc2019.d03 import FindNearestIntsection, FindShortestIntersection
from tools.paths import Point


class TestNearestDistance(TestCase):
    def test_example1(self):
        vectorsA=["R8","U5", "L5", "D3"]
        vectorsB=["U7", "R6", "D4", "L4"]
        self.assertEqual(Point(3,3), FindNearestIntsection(vectorsA, vectorsB).GetPoint())

    def test_example2(self):
        vectorsA=["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
        vectorsB=["U62","R66","U55","R34","D71","R55","D58","R83"]
        self.assertEqual(Point(155,4), FindNearestIntsection(vectorsA, vectorsB).GetPoint())

    def test_example3(self):
        vectorsA=["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
        vectorsB=["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
        self.assertEqual(Point(124,11), FindNearestIntsection(vectorsA, vectorsB).GetPoint())

class TestShortestDistance(TestCase):
    def test_example1(self):
        vectorsA=["R8","U5", "L5", "D3"]
        vectorsB=["U7", "R6", "D4", "L4"]
        self.assertEqual(30, FindShortestIntersection(vectorsA, vectorsB).pathLen)

    def test_example2(self):
        vectorsA=["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
        vectorsB=["U62","R66","U55","R34","D71","R55","D58","R83"]
        self.assertEqual(610, FindShortestIntersection(vectorsA, vectorsB).pathLen)

    def test_example3(self):
        vectorsA=["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
        vectorsB=["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
        self.assertEqual(410, FindShortestIntersection(vectorsA, vectorsB).pathLen)
