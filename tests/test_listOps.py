from tools.listOps import NonSortedIntersection, NonSortedMatchGroups
from tools.paths import Point, PathPoint
from unittest import TestCase

class TestIntersect(TestCase):
    def test_NoKey(self):
        listA = [1,2,3,4,5,6]
        listB = [7,8,9,8,7,6,5,4,1]
        self.assertListEqual(NonSortedIntersection(listA, listB), [1,4,5,6])

    def test_Repeats_onerepeating(self):
        listA = [1,2,3,4]
        listB = [1,1,2,2,3,3,3,4,4,4,5,5,6]
        self.assertListEqual(NonSortedIntersection(listA, listB), [1,2,3,4])

    def test_Repeats_bothrepeating(self):
        listA = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,4]
        listB = [1,1,2,2,3,3,3,4,4,4,5,5,6]
        self.assertListEqual(NonSortedIntersection(listA, listB), [1,2,3,4])

    def test_Repeats_bothrepeating_custSort(self):
        listA = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,4]
        listB = [1,1,2,2,3,3,3,4,4,4,5,5,6]

        key = lambda x: x
        self.assertListEqual(NonSortedIntersection(listA, listB, key=key), [1,2,3,4])

    def test_Repeats_ObjectSort(self):
        listA = [Point(1,1), Point(2,2), Point(0,1)]
        listB = [Point(3,3), Point(1,1), Point(0,1)]

        self.assertListEqual(NonSortedIntersection(listA, listB), [Point(0, 1), Point(1, 1)])

    def test_CustomEq(self):
        listA = [PathPoint(1,1,0), PathPoint(2,2,0), PathPoint(0,1,0)]
        listB = [PathPoint(3,3,1), PathPoint(1,1,1), PathPoint(0,1,1)]

        key = lambda p: p.GetPoint()

        self.assertListEqual(NonSortedIntersection(listA, listB, key=key), [PathPoint(0, 1, 0), PathPoint(1, 1, 0)])

class TestIntersectGroups(TestCase):
    def test_NoKey(self):
        listA = [1,2,3,4,5,6]
        listB = [7,8,9,8,7,6,5,4,1]
        matches = [
            ([1], [1]),
            ([4], [4]),
            ([5], [5]),
            ([6], [6]),
        ]
        self.assertListEqual(NonSortedMatchGroups(listA, listB), matches)

    def test_MultiOneList(self):
        listA = [1,2,3,4,5,6]
        listB = [4,4,4,4,3,3,3,2,2,1]
        matches = [
            ([1], [1]),
            ([2], [2,2]),
            ([3], [3,3,3]),
            ([4], [4,4,4,4]),
        ]
        self.assertListEqual(NonSortedMatchGroups(listA, listB), matches)

    def test_MultiOtherList(self):
        listB = [1,2,3,4,5,6]
        listA = [4,4,4,4,3,3,3,2,2,1]
        matches = [
            ([1], [1]),
            ([2,2], [2]),
            ([3,3,3], [3]),
            ([4,4,4,4], [4]),
        ]
        self.assertListEqual(NonSortedMatchGroups(listA, listB), matches)

    def test_MultiBothLists(self):
        listB = [1,1,2,2,2,3,3,3,3,4,4,4,4,4]
        listA = [4,4,4,4,3,3,3,2,2,1]

        matches = [
            ([1], [1,1]),
            ([2,2], [2,2,2]),
            ([3,3,3], [3,3,3,3]),
            ([4,4,4,4], [4,4,4,4,4]),
        ]
        self.assertListEqual(NonSortedMatchGroups(listA, listB), matches)

    def test_SortKey(self):
        listA = [PathPoint(1, 1, 0), PathPoint(2, 2, 0), PathPoint(0, 1, 0)]
        listB = [PathPoint(3, 3, 1), PathPoint(1, 1, 1), PathPoint(0, 1, 1), PathPoint(1, 1, 1)]

        key = lambda p: p.GetPoint()

        matches = [
            ([PathPoint(0, 1, 0)], [PathPoint(0, 1, 1)]),
            ([PathPoint(1, 1, 0)], [PathPoint(1, 1, 1), PathPoint(1, 1, 1)]),
        ]

        self.assertListEqual(NonSortedMatchGroups(listA, listB, key=key), matches)

