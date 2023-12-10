from unittest import TestCase

from aoc2023.d10 import make_segment, traverse_pipe, EnterFrom, NextSegment
from aoc2023.d10 import PipeSegment, load_grid, determine_start, load_grid_with_start
from aoc2023.d10 import part_one, load_enclosure, is_enclosed
from aoc2023.d10 import count_enclosed_area
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


def do_traversal(enter_from: EnterFrom, segment: PipeSegment) -> NextSegment:
    enter_from = NextSegment(x=5, y=5, enter_from=enter_from)
    return traverse_pipe(enter_from, segment)


class TestSegment(TestCase):

    def check_errors(self, segment: PipeSegment, direction: EnterFrom):
        enter_from = NextSegment(x=5, y=5, enter_from=direction)
        with self.assertRaises(ValueError):
            traverse_pipe(enter_from, segment)

    def test_vertical(self):
        segment = make_segment("|")
        self.check_errors(segment, EnterFrom.LEFT)
        self.check_errors(segment, EnterFrom.RIGHT)

        self.assertEqual(do_traversal(EnterFrom.TOP, segment),
                         NextSegment(x=5, y=6, enter_from=EnterFrom.TOP))

        self.assertEqual(do_traversal(EnterFrom.BOTTOM, segment),
                         NextSegment(x=5, y=4, enter_from=EnterFrom.BOTTOM))

    def test_horizontal(self):
        segment = make_segment("-")
        self.check_errors(segment, EnterFrom.TOP)
        self.check_errors(segment, EnterFrom.BOTTOM)

        self.assertEqual(do_traversal(EnterFrom.LEFT, segment),
                         NextSegment(x=6, y=5, enter_from=EnterFrom.LEFT))

        self.assertEqual(do_traversal(EnterFrom.RIGHT, segment),
                         NextSegment(x=4, y=5, enter_from=EnterFrom.RIGHT))

    def test_L(self):
        segment = make_segment("L")
        self.check_errors(segment, EnterFrom.LEFT)
        self.check_errors(segment, EnterFrom.BOTTOM)

        self.assertEqual(do_traversal(EnterFrom.RIGHT, segment),
                         NextSegment(x=5, y=4, enter_from=EnterFrom.BOTTOM))

        self.assertEqual(do_traversal(EnterFrom.TOP, segment),
                         NextSegment(x=6, y=5, enter_from=EnterFrom.LEFT))

    def test_J(self):
        segment = make_segment("J")
        self.check_errors(segment, EnterFrom.BOTTOM)
        self.check_errors(segment, EnterFrom.RIGHT)

        self.assertEqual(do_traversal(EnterFrom.LEFT, segment),
                         NextSegment(x=5, y=4, enter_from=EnterFrom.BOTTOM))

        self.assertEqual(do_traversal(EnterFrom.TOP, segment),
                         NextSegment(x=4, y=5, enter_from=EnterFrom.RIGHT))

    def test_7(self):
        segment = make_segment("7")
        self.check_errors(segment, EnterFrom.TOP)
        self.check_errors(segment, EnterFrom.RIGHT)

        self.assertEqual(do_traversal(EnterFrom.LEFT, segment),
                         NextSegment(x=5, y=6, enter_from=EnterFrom.TOP))

        self.assertEqual(do_traversal(EnterFrom.BOTTOM, segment),
                         NextSegment(x=4, y=5, enter_from=EnterFrom.RIGHT))

    def test_F(self):
        segment = make_segment("F")
        self.check_errors(segment, EnterFrom.LEFT)
        self.check_errors(segment, EnterFrom.TOP)

        self.assertEqual(do_traversal(EnterFrom.RIGHT, segment),
                         NextSegment(x=5, y=6, enter_from=EnterFrom.TOP))

        self.assertEqual(do_traversal(EnterFrom.BOTTOM, segment),
                         NextSegment(x=6, y=5, enter_from=EnterFrom.LEFT))


class TestLoad(TestCase):
    def test_simplest_loop(self):
        grid = load_grid(get_test_file_path("samples/d10/simplest_loop.txt"))
        self.assertIsNone(grid[0][0])
        self.assertEqual(grid[1][1], make_segment("F"))

    def test_simplest_loop_start(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/simplest_start.txt"))
        self.assertIsNone(grid.pipes[0][0])
        self.assertEqual(grid.pipes[1][1], make_segment("F"))
        self.assertEqual(grid.start_x, 1)
        self.assertEqual(grid.start_y, 1)

    def test_starts(self):
        grid = load_grid(get_test_file_path("samples/d10/starts.txt"))
        self.assertEqual(determine_start(grid, 1, 1), make_segment("F"))
        self.assertEqual(determine_start(grid, 2, 1), make_segment("-"))
        self.assertEqual(determine_start(grid, 3, 1), make_segment("7"))
        self.assertEqual(determine_start(grid, 1, 2), make_segment("|"))
        self.assertEqual(determine_start(grid, 1, 3), make_segment("|"))
        self.assertEqual(determine_start(grid, 1, 4), make_segment("L"))
        self.assertEqual(determine_start(grid, 3, 4), make_segment("J"))
        pass


class FurthestPoint(TestCase):
    def test_simplest_loop(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/simplest_start.txt"))
        self.assertEqual(part_one(grid), 4)

    def test_complex_loop(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/complext_start.txt"))
        self.assertEqual(part_one(grid), 8)


class Enclosure(TestCase):
    def test_outter_cells(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        self.assertFalse(is_enclosed(cells, 0, 0))
        self.assertFalse(is_enclosed(cells, 5, 8))

    def test_fully_enclosed(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        self.assertTrue(is_enclosed(cells, 3, 6))

    def test_gap_to_bottom(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        self.assertFalse(is_enclosed(cells, 5, 6))

    def test_compromised_box(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        self.assertFalse(is_enclosed(cells, 3, 4))

    def test_example_one(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        self.assertEqual(count_enclosed_area(cells), 4)
