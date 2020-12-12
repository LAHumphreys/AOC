from unittest import TestCase

from aoc2020.d11 import load_state, SeatState, single_step, count_adjacent_occupied
from aoc2020.d11 import loop_until_stable, number_seated, count_next_occupied, loop_until_stable_part_2
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class TestPart1(TestCase):

    def test_initial_state(self):
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(10, len(initial_state))
        firstRow = [
            SeatState.EMPTY,
            SeatState.NO_SEAT,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.NO_SEAT,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.NO_SEAT,
            SeatState.EMPTY,
            SeatState.EMPTY,
        ]
        lastRow = [
            SeatState.EMPTY,
            SeatState.NO_SEAT,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.EMPTY,
            SeatState.NO_SEAT,
            SeatState.EMPTY,
            SeatState.EMPTY,
        ]
        self.assertListEqual(firstRow, initial_state[0])
        self.assertListEqual(lastRow, initial_state[-1])

    def test_single_count_empty(self):
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(count_adjacent_occupied(initial_state, 0, 0), 0)
        self.assertEqual(count_adjacent_occupied(initial_state, 1, 1), 0)
        self.assertEqual(count_adjacent_occupied(initial_state, 2, 2), 0)
        self.assertEqual(count_adjacent_occupied(initial_state, 9, 9), 0)
        self.assertEqual(count_adjacent_occupied(initial_state, 0, 9), 0)
        self.assertEqual(count_adjacent_occupied(initial_state, 9, 0), 0)

    def test_single_count_filled(self):
        initial_state_path = GetTestFilePath("samples/d11/sample1_firstitter.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(count_adjacent_occupied(initial_state, 0, 0), 2)
        self.assertEqual(count_adjacent_occupied(initial_state, 0, 9), 3)
        self.assertEqual(count_adjacent_occupied(initial_state, 9, 9), 2)
        self.assertEqual(count_adjacent_occupied(initial_state, 9, 0), 1)
        self.assertEqual(count_adjacent_occupied(initial_state, 3, 3), 5)

    def test_single_step(self):
        self.maxDiff = None
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        first_step_path = GetTestFilePath("samples/d11/sample1_firstitter.txt")
        initial_state = load_state(initial_state_path)
        expected_first_step = load_state(first_step_path)
        first_step = single_step(initial_state)[0]
        self.assertListEqual(expected_first_step, first_step)

    def test_second_step(self):
        self.maxDiff = None
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        second_step_path = GetTestFilePath("samples/d11/sample1_second_step.txt")
        initial_state = load_state(initial_state_path)
        expected_second_step = load_state(second_step_path)
        first_step = single_step(initial_state)[0]
        second_step = single_step(first_step)[0]
        self.assertListEqual(expected_second_step, second_step)

    def test_continue_until_stable(self):
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        final_step_path = GetTestFilePath("samples/d11/sample1_final_state.txt")
        initial_state = load_state(initial_state_path)
        expected_final_state = load_state(final_step_path)
        final_state = loop_until_stable(initial_state)
        self.maxDiff = None
        self.assertListEqual(expected_final_state, final_state)
        self.assertEqual(37, number_seated(final_state))


class TestPart2(TestCase):
    def test_single_count_filled(self):
        initial_state_path = GetTestFilePath("samples/d11/sample2.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(count_next_occupied(initial_state, 4, 3), 8)

    def test_single_count_empty(self):
        initial_state_path = GetTestFilePath("samples/d11/sample3.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(count_next_occupied(initial_state, 1, 1), 0)
        self.assertEqual(count_next_occupied(initial_state, 1, 3), 1)

    def test_single_count_all_filled(self):
        initial_state_path = GetTestFilePath("samples/d11/sample4.txt")
        initial_state = load_state(initial_state_path)
        self.assertEqual(count_next_occupied(initial_state, 3, 3), 0)

    def test_continue_until_stable(self):
        initial_state_path = GetTestFilePath("samples/d11/sample1.txt")
        final_step_path = GetTestFilePath("samples/d11/sample1_final_mode2.txt")
        initial_state = load_state(initial_state_path)
        expected_final_state = load_state(final_step_path)
        final_state = loop_until_stable_part_2(initial_state)
        self.maxDiff = None
        self.assertListEqual(expected_final_state, final_state)
        self.assertEqual(26, number_seated(final_state))
