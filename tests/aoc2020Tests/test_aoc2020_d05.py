from unittest import TestCase

from aoc2020.d05 import chop, get_all_seats, get_seat


class Test_Part1(TestCase):
    def test_example1(self):
        (row, col, seat_id) = get_seat("BFFFBBFRRR")
        self.assertEqual(row, 70)
        self.assertEqual(col, 7)
        self.assertEqual(seat_id, 567)

    def test_example2(self):
        (row, col, seat_id) = get_seat("FFFBBBFRRR")
        self.assertEqual(row, 14)
        self.assertEqual(col, 7)
        self.assertEqual(seat_id, 119)

    def test_example3(self):
        (row, col, seat_id) = get_seat("BBFFBBFRLL")
        self.assertEqual(row, 102)
        self.assertEqual(col, 4)
        self.assertEqual(seat_id, 820)

    def test_getSeats(self):
        rows = [x for x in range(128)]
        cols = [c for c in range(8)]
        self.assertListEqual(get_all_seats()[0], rows)
        self.assertListEqual(get_all_seats()[1], cols)

    def test_FirstTest(self):
        (rows, cols) = chop(get_all_seats(), "F")
        self.assertListEqual(rows, [x for x in range(64)])
        self.assertListEqual(cols, [x for x in range(8)])

    def test_BottomHalf(self):
        (rows, cols) = chop(get_all_seats(), "B")
        self.assertListEqual(rows, [x for x in range(64, 128)])
        self.assertListEqual(cols, [x for x in range(8)])

    def test_LeftHalf(self):
        (rows, cols) = chop(get_all_seats(), "L")
        self.assertListEqual(rows, [x for x in range(128)])
        self.assertListEqual(cols, [0, 1, 2, 3])

    def test_RightHalf(self):
        (rows, cols) = chop(get_all_seats(), "R")
        self.assertListEqual(rows, [x for x in range(128)])
        self.assertListEqual(cols, [4, 5, 6, 7])
