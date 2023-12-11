from unittest import TestCase

from aoc2023.d10 import make_segment, traverse_pipe, EnterFrom, NextSegment
from aoc2023.d10 import apply_pipe_to_edges, Edge, mark_outer_edges
from aoc2023.d10 import PipeSegment, load_grid, determine_start, load_grid_with_start
from aoc2023.d10 import part_one, load_enclosure, PipeEnclosureState, draw_loop, debug_print
from aoc2023.d10 import count_enclosed_area, expose_cell, resolve_marked_exposures, mark_edges, part_two
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

    def test_vertical_edges(self):
        # No Rotation
        self.assertEqual(apply_pipe_to_edges(Edge.LEFT, make_segment("|"), Edge.TOP), Edge.LEFT)
        self.assertEqual(apply_pipe_to_edges(Edge.RIGHT, make_segment("|"), Edge.BOTTOM), Edge.RIGHT)

    def test_horizontal(self):
        segment = make_segment("-")
        self.check_errors(segment, EnterFrom.TOP)
        self.check_errors(segment, EnterFrom.BOTTOM)

        self.assertEqual(do_traversal(EnterFrom.LEFT, segment),
                         NextSegment(x=6, y=5, enter_from=EnterFrom.LEFT))

        self.assertEqual(do_traversal(EnterFrom.RIGHT, segment),
                         NextSegment(x=4, y=5, enter_from=EnterFrom.RIGHT))

    def test_horizontal_edges(self):
        # No Rotation
        self.assertEqual(apply_pipe_to_edges(Edge.TOP, make_segment("-"), Edge.LEFT), Edge.TOP)
        self.assertEqual(apply_pipe_to_edges(Edge.BOTTOM, make_segment("-"), Edge.RIGHT), Edge.BOTTOM)

    def test_L(self):
        segment = make_segment("L")
        self.check_errors(segment, EnterFrom.LEFT)
        self.check_errors(segment, EnterFrom.BOTTOM)

        self.assertEqual(do_traversal(EnterFrom.RIGHT, segment),
                         NextSegment(x=5, y=4, enter_from=EnterFrom.BOTTOM))

        self.assertEqual(do_traversal(EnterFrom.TOP, segment),
                         NextSegment(x=6, y=5, enter_from=EnterFrom.LEFT))

    def test_L_edges(self):
        self.assertEqual(apply_pipe_to_edges(Edge.TOP, make_segment("L"), EnterFrom.RIGHT), Edge.RIGHT)
        self.assertEqual(apply_pipe_to_edges(Edge.BOTTOM, make_segment("L"), EnterFrom.RIGHT), Edge.LEFT)
        self.assertEqual(apply_pipe_to_edges(Edge.LEFT, make_segment("L"), EnterFrom.TOP), Edge.BOTTOM)
        self.assertEqual(apply_pipe_to_edges(Edge.RIGHT, make_segment("L"), EnterFrom.TOP), Edge.TOP)

    def test_J_edges(self):
        self.assertEqual(apply_pipe_to_edges(Edge.TOP, make_segment("J"), EnterFrom.LEFT), Edge.LEFT)
        self.assertEqual(apply_pipe_to_edges(Edge.BOTTOM, make_segment("J"), EnterFrom.LEFT), Edge.RIGHT)
        self.assertEqual(apply_pipe_to_edges(Edge.LEFT, make_segment("J"), EnterFrom.TOP), Edge.TOP)
        self.assertEqual(apply_pipe_to_edges(Edge.RIGHT, make_segment("J"), EnterFrom.TOP), Edge.BOTTOM)

    def test_F_edges(self):
        self.assertEqual(apply_pipe_to_edges(Edge.TOP, make_segment("F"), EnterFrom.RIGHT), Edge.LEFT)
        self.assertEqual(apply_pipe_to_edges(Edge.BOTTOM, make_segment("F"), EnterFrom.RIGHT), Edge.RIGHT)
        self.assertEqual(apply_pipe_to_edges(Edge.LEFT, make_segment("F"), EnterFrom.BOTTOM), Edge.TOP)
        self.assertEqual(apply_pipe_to_edges(Edge.RIGHT, make_segment("F"), EnterFrom.BOTTOM), Edge.BOTTOM)

    def test_7_edges(self):
        self.assertEqual(apply_pipe_to_edges(Edge.TOP, make_segment("7"), EnterFrom.LEFT), Edge.RIGHT)
        self.assertEqual(apply_pipe_to_edges(Edge.BOTTOM, make_segment("7"), EnterFrom.LEFT), Edge.LEFT)
        self.assertEqual(apply_pipe_to_edges(Edge.LEFT, make_segment("7"), EnterFrom.BOTTOM), Edge.BOTTOM)
        self.assertEqual(apply_pipe_to_edges(Edge.RIGHT, make_segment("7"), EnterFrom.BOTTOM), Edge.TOP)

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


class Exposure(TestCase):
    def test_outter_cells_left_corner(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        expose_cell(cells, 0, 0)
        debug_print(cells)
        # Cell itself is exposed
        self.assertEqual(cells[0][0], PipeEnclosureState.EXPOSED)
        # Cells with no further propagation are also exposed
        # *+*******++
        # .F-------7.
        self.assertEqual(cells[0][1], PipeEnclosureState.MARKED)
        self.assertEqual(cells[0][2], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[0][3], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[0][5], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[0][8], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[0][10], PipeEnclosureState.MARKED)
        self.assertEqual(cells[0][9], PipeEnclosureState.MARKED)

        self.assertEqual(cells[1][0], PipeEnclosureState.MARKED)
        self.assertEqual(cells[2][0], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[5][0], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[7][0], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][0], PipeEnclosureState.MARKED)

    def test_outter_cells_right_corner(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        expose_cell(cells, 10, 8)
        debug_print(cells)

        self.assertEqual(cells[8][9], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][8], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[8][7], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[8][6], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][5], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][4], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][3], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[8][2], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[8][1], PipeEnclosureState.MARKED)
        self.assertEqual(cells[8][0], PipeEnclosureState.MARKED)

        self.assertEqual(cells[7][10], PipeEnclosureState.MARKED)
        self.assertEqual(cells[6][10], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[5][10], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[4][10], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[3][10], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[2][10], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[1][10], PipeEnclosureState.MARKED)
        self.assertEqual(cells[0][10], PipeEnclosureState.MARKED)

    def test_horizontal_double_gap_block(self):
        cells = load_enclosure(get_test_file_path("samples/d10/larger_enclosed_example.txt"))
        expose_cell(cells, 19, 4)
        self.assertEqual(cells[4][19], PipeEnclosureState.EXPOSED)
        self.assertEqual(cells[4][9], PipeEnclosureState.UNTESTED)


class PipeWalk(TestCase):
    def test_draw_loop(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/main_enclosure_example.txt"))
        self.assertEqual(part_two(grid), 10)

    def test_mark_outter_edges(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/simplest_start.txt"))
        enclosure = draw_loop(grid)
        debug_print(enclosure)
        mark_outer_edges(enclosure, grid)
        debug_print(enclosure)
        self.assertEqual(enclosure[0][1], PipeEnclosureState.MARKED)


class Enclosure(TestCase):
    def test_example_one(self):
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        mark_edges(cells)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 4)

    def test_example_one_outter(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/enclosed_example_.txt"))
        cells = load_enclosure(get_test_file_path("samples/d10/enclosed_example_.txt"))
        debug_print(cells)
        mark_outer_edges(cells, grid)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 4)

    def test_example_two(self):
        cells = load_enclosure(get_test_file_path("samples/d10/second_enclosed_example.txt"))
        mark_edges(cells)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 4)

    def test_example_two_outter(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/second_enclosed_example.txt"))
        cells = load_enclosure(get_test_file_path("samples/d10/second_enclosed_example.txt"))
        mark_outer_edges(cells, grid)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 4)

    def test_example_three(self):
        cells = load_enclosure(get_test_file_path("samples/d10/larger_enclosed_example.txt"))
        mark_edges(cells)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 8)

    def test_example_three_outter(self):
        grid = load_grid_with_start(get_test_file_path("samples/d10/larger_enclosed_example.txt"))
        cells = load_enclosure(get_test_file_path("samples/d10/larger_enclosed_example.txt"))
        debug_print(cells)
        mark_outer_edges(cells, grid)
        debug_print(cells)
        resolve_marked_exposures(cells)
        self.assertEqual(count_enclosed_area(cells), 8)

