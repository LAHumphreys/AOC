import copy
from unittest import TestCase

from tools.listOps import non_sorted_intersection, unsorted_matched_groups, find_sum_pair, ListTooShort, find_sum_trio
from tools.paths import Point, PathPoint


class TestIntersect(TestCase):
    def test_NoKey(self):
        listA = [1, 2, 3, 4, 5, 6]
        listB = [7, 8, 9, 8, 7, 6, 5, 4, 1]
        self.assertListEqual(non_sorted_intersection(listA, listB), [1, 4, 5, 6])

    def test_Repeats_onerepeating(self):
        listA = [1, 2, 3, 4]
        listB = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
        self.assertListEqual(non_sorted_intersection(listA, listB), [1, 2, 3, 4])

    def test_Repeats_bothrepeating(self):
        listA = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4]
        listB = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
        self.assertListEqual(non_sorted_intersection(listA, listB), [1, 2, 3, 4])

    def test_Repeats_bothrepeating_custSort(self):
        listA = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4]
        listB = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]

        def key(x): return x

        self.assertListEqual(
            non_sorted_intersection(
                listA, listB, key=key), [
                1, 2, 3, 4])

    def test_Repeats_ObjectSort(self):
        listA = [Point(1, 1), Point(2, 2), Point(0, 1)]
        listB = [Point(3, 3), Point(1, 1), Point(0, 1)]

        self.assertListEqual(
            non_sorted_intersection(
                listA, listB), [
                Point(
                    0, 1), Point(
                    1, 1)])

    def test_CustomEq(self):
        listA = [PathPoint(1, 1, 0), PathPoint(2, 2, 0), PathPoint(0, 1, 0)]
        listB = [PathPoint(3, 3, 1), PathPoint(1, 1, 1), PathPoint(0, 1, 1)]

        def key(p): return p.get_point()

        self.assertListEqual(
            non_sorted_intersection(
                listA, listB, key=key), [
                PathPoint(
                    0, 1, 0), PathPoint(
                    1, 1, 0)])


class TestIntersectGroups(TestCase):
    def test_NoKey(self):
        listA = [1, 2, 3, 4, 5, 6]
        listB = [7, 8, 9, 8, 7, 6, 5, 4, 1]
        matches = [
            ([1], [1]),
            ([4], [4]),
            ([5], [5]),
            ([6], [6]),
        ]
        self.assertListEqual(unsorted_matched_groups(listA, listB), matches)

    def test_MultiOneList(self):
        listA = [1, 2, 3, 4, 5, 6]
        listB = [4, 4, 4, 4, 3, 3, 3, 2, 2, 1]
        matches = [
            ([1], [1]),
            ([2], [2, 2]),
            ([3], [3, 3, 3]),
            ([4], [4, 4, 4, 4]),
        ]
        self.assertListEqual(unsorted_matched_groups(listA, listB), matches)

    def test_MultiOtherList(self):
        listB = [1, 2, 3, 4, 5, 6]
        listA = [4, 4, 4, 4, 3, 3, 3, 2, 2, 1]
        matches = [
            ([1], [1]),
            ([2, 2], [2]),
            ([3, 3, 3], [3]),
            ([4, 4, 4, 4], [4]),
        ]
        self.assertListEqual(unsorted_matched_groups(listA, listB), matches)

    def test_MultiBothLists(self):
        listB = [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4]
        listA = [4, 4, 4, 4, 3, 3, 3, 2, 2, 1]

        matches = [
            ([1], [1, 1]),
            ([2, 2], [2, 2, 2]),
            ([3, 3, 3], [3, 3, 3, 3]),
            ([4, 4, 4, 4], [4, 4, 4, 4, 4]),
        ]
        self.assertListEqual(unsorted_matched_groups(listA, listB), matches)

    def test_SortKey(self):
        listA = [PathPoint(1, 1, 0), PathPoint(2, 2, 0), PathPoint(0, 1, 0)]
        listB = [
            PathPoint(
                3, 3, 1), PathPoint(
                1, 1, 1), PathPoint(
                0, 1, 1), PathPoint(
                1, 1, 1)]

        def key(p): return p.get_point()

        matches = [
            ([PathPoint(0, 1, 0)], [PathPoint(0, 1, 1)]),
            ([PathPoint(1, 1, 0)], [PathPoint(1, 1, 1), PathPoint(1, 1, 1)]),
        ]

        self.assertListEqual(
            unsorted_matched_groups(
                listA, listB, key=key), matches)


class TestFindSumPair(TestCase):
    def test_EmptyList(self):
        self.assertRaises(ListTooShort, lambda: find_sum_pair([], 0))
        self.assertRaises(ListTooShort, lambda: find_sum_pair([0], 0))

    def test_First(self):
        self.assertListEqual(find_sum_pair([1, 2, 3, 4], 3), [1, 2])

    def test_Last(self):
        self.assertListEqual(find_sum_pair([1, 2, 3, 4], 7), [3, 4])

    def test_FirstAndLast(self):
        self.assertListEqual(find_sum_pair([1, 2, 3, 7], 8), [1, 7])

    def test_MiddleAndLast(self):
        numbers = [1, 2, 3, 5, 7, 11, 13, 17, 23]
        self.assertListEqual(find_sum_pair(numbers, 16), [3, 13])

    def test_NoPair(self):
        self.assertIsNone(find_sum_pair([1, 2, 3], -1))

    def test_MiddleAndLast_SortRequired(self):
        numbers = [13, 23, 17, 1, 3, 2, 5, 7, 11]
        backupNumbers = copy.copy(numbers)
        self.assertListEqual(find_sum_pair(numbers, 16), [3, 13])
        self.assertListEqual(numbers, backupNumbers)

    def test_PuzzleInput(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertListEqual(find_sum_pair(numbers, 2020), [299, 1721])


class TestFindSumTrio(TestCase):
    def test_EmptyList(self):
        self.assertRaises(ListTooShort, lambda: find_sum_trio([], 0))
        self.assertRaises(ListTooShort, lambda: find_sum_trio([0], 0))
        self.assertRaises(ListTooShort, lambda: find_sum_trio([0, 1], 0))

    def test_First(self):
        self.assertListEqual(find_sum_trio([1, 2, 3, 4], 6), [1, 2, 3])

    def test_Last(self):
        self.assertListEqual(find_sum_trio([1, 2, 3, 4], 9), [2, 3, 4])

    def test_NoPair(self):
        self.assertIsNone(find_sum_trio([1, 2, 3, 4, 5], -1))

    def test_MiddleAndLast(self):
        numbers = [1, 2, 3, 5, 7, 11, 13, 14]
        self.assertListEqual(find_sum_trio(numbers, 23), [2, 7, 14])

    def test_MiddleAndLast_SortRequired(self):
        numbers = [13, 11, 7, 1, 3, 2, 14, 5]
        backupNumbers = copy.copy(numbers)
        self.assertListEqual(find_sum_trio(numbers, 23), [2, 7, 14])
        self.assertListEqual(numbers, backupNumbers)

    def test_PuzzleInput(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertListEqual(find_sum_trio(numbers, 2020), [366, 675, 979])
