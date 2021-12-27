from unittest import TestCase

from aoc2021.d22 import parse_cube_defn, SwitchMode, load_cubes, SwitchCube, count_points
from aoc2021.d22 import cubes_overlap, get_ref_cube, consolidate_cubes
from aoc2021.d22 import get_volume_cube, make_hole, merge_cubes, get_total_volume
from aoc2021.d22 import split_composite_to_cubes, count_all_points
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Composites(TestCase):
    def test_not_overlapping(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=11..20,y=11..20,z=11..20")
        expected = [
             parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
             parse_cube_defn("on x=11..20,y=11..20,z=11..20")
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))

    def test_contained_within(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=1..2,y=1..2,z=1..2")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_sticking_out_top(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=1..2,y=1..2,z=1..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=1..2,y=1..2,z=11..12"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_sticking_out_top_bottom(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=1..2,y=1..2,z=-3..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=1..2,y=1..2,z=11..12"),
            parse_cube_defn("on x=1..2,y=1..2,z=-3..-1"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_sticking_out_left_right_(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=-3..12,y=1..2,z=1..2")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=11..12,y=1..2,z=1..2"),
            parse_cube_defn("on x=-3..-1,y=1..2,z=1..2"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_sticking_out_front_back(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=1..2,y=-3..12,z=1..2")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=1..2,y=11..12,z=1..2"),
            parse_cube_defn("on x=1..2,y=-3..-1,z=1..2"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_corner_top_front_right(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=9..12,y=9..12,z=9..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=9..10,y=9..10,z=11..12"),
            parse_cube_defn("on x=9..10,y=11..12,z=9..12"),
            parse_cube_defn("on x=11..12,y=9..12,z=9..12"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_corners_top(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=-2..12,y=-2..12,z=9..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=0..10,y=0..10,z=11..12"),
            parse_cube_defn("on x=0..10,y=11..12,z=9..12"),
            parse_cube_defn("on x=0..10,y=-2..-1,z=9..12"),
            parse_cube_defn("on x=11..12,y=-2..12,z=9..12"),
            parse_cube_defn("on x=-2..-1,y=-2..12,z=9..12"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_corners_bottom(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=-2..12,y=-2..12,z=-2..1")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),
            parse_cube_defn("on x=0..10,y=0..10,z=-2..-1"),
            parse_cube_defn("on x=0..10,y=11..12,z=-2..1"),
            parse_cube_defn("on x=0..10,y=-2..-1,z=-2..1"),
            parse_cube_defn("on x=11..12,y=-2..12,z=-2..1"),
            parse_cube_defn("on x=-2..-1,y=-2..12,z=-2..1"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_corners_right(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=9..12,y=-2..12,z=-2..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),

            parse_cube_defn("on x=9..10,y=0..10,z=11..12"),
            parse_cube_defn("on x=9..10,y=0..10,z=-2..-1"),

            parse_cube_defn("on x=9..10,y=11..12,z=-2..12"),
            parse_cube_defn("on x=9..10,y=-2..-1,z=-2..12"),

            parse_cube_defn("on x=11..12,y=-2..12,z=-2..12"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))

    def test_corners_front(self):
        first = parse_cube_defn("on x=0..10,y=0..10,z=0..10")
        second = parse_cube_defn("on x=-2..12,y=9..12,z=-2..12")
        expected = [
            parse_cube_defn("on x=0..10,y=0..10,z=0..10"),

            parse_cube_defn("on x=0..10,y=9..10,z=11..12"),
            parse_cube_defn("on x=0..10,y=9..10,z=-2..-1"),

            parse_cube_defn("on x=0..10,y=11..12,z=-2..12"),

            parse_cube_defn("on x=11..12,y=9..12,z=-2..12"),
            parse_cube_defn("on x=-2..-1,y=9..12,z=-2..12"),
        ]
        self.assertListEqual(expected, split_composite_to_cubes(first, second))
        self.assertListEqual(expected, split_composite_to_cubes(second, first))



class Loader(TestCase):
    def test_load_on(self):
        cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        self.assertEqual(cube.mode, SwitchMode.ON)
        self.assertEqual(cube.min_x, 10)
        self.assertEqual(cube.max_x, 12)
        self.assertEqual(cube.min_y, 10)
        self.assertEqual(cube.max_y, 12)
        self.assertEqual(cube.min_z, 10)
        self.assertEqual(cube.max_z, 12)

    def test_load_off(self):
        cube = parse_cube_defn("off x=-48..-32,y=-32..-16,z=-15..-5")
        self.assertEqual(cube.mode, SwitchMode.OFF)
        self.assertEqual(cube.min_x, -48)
        self.assertEqual(cube.max_x, -32)
        self.assertEqual(cube.min_y, -32)
        self.assertEqual(cube.max_y, -16)
        self.assertEqual(cube.min_z, -15)
        self.assertEqual(cube.max_z, -5)

    def test_load(self):
        cubes = load_cubes(get_test_file_path("samples/d22/small.txt"))
        self.assertEqual(len(cubes), 4)
        expected = [
            SwitchCube(mode=SwitchMode.ON,  min_x=10, max_x=12, min_y=10, max_y=12, min_z=10, max_z=12, holes=[]),
            SwitchCube(mode=SwitchMode.ON,  min_x=11, max_x=13, min_y=11, max_y=13, min_z=11, max_z=13, holes=[]),
            SwitchCube(mode=SwitchMode.OFF, min_x=9,  max_x=11, min_y=9,  max_y=11, min_z=9,  max_z=11, holes=[]),
            SwitchCube(mode=SwitchMode.ON,  min_x=10, max_x=10, min_y=10, max_y=10, min_z=10, max_z=10, holes=[])
        ]
        self.assertListEqual(expected, cubes)


class TestOverlap(TestCase):
    def test_no_overlap_examples(self):
        ref_cube = get_ref_cube()
        self.assertFalse(cubes_overlap(parse_cube_defn("on x=-54112..-39298,y=-85059..-49293,z=-27449..7877"), ref_cube))
        self.assertFalse(cubes_overlap(parse_cube_defn("on x=967..23432,y=45373..81175,z=27513..53682"), ref_cube))

    def test_overlap_examples(self):
        ref_cube = get_ref_cube()
        self.assertTrue(cubes_overlap(parse_cube_defn("on x=-20..26,y=-36..17,z=-47..7"), ref_cube))
        self.assertTrue(cubes_overlap(parse_cube_defn("on x=-20..33,y=-21..23,z=-26..28"), ref_cube))

    def test_z_below(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=-20..26,y=-36..17,z=-60..-51")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))

    def test_z_above(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=-20..26,y=-36..17,z=51..60")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))

    def test_x_below(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=-60..-51,y=-36..17,z=1..2")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))

    def test_x_above(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=51..50,y=-36..17,z=-20..26")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))

    def test_y_below(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=-20..26,y=-60..-51,z=-36..17")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))

    def test_y_above(self):
        ref_cube = get_ref_cube()
        other_cube = parse_cube_defn("on x=-20..26,y=51..50,z=-36..17")
        self.assertFalse(cubes_overlap(ref_cube, other_cube))


class OnOff(TestCase):
    def test_count_cubes(self):
        cubes = load_cubes(get_test_file_path("samples/d22/small.txt"))
        self.assertEqual(39, count_points(cubes))
        self.assertEqual(39, count_all_points(cubes))

    def test_count_large_cubes(self):
        cubes = load_cubes(get_test_file_path("samples/d22/large.txt"))
        self.assertEqual(590784, count_points(cubes))
        pass

    def test_count_huge_cubes(self):
        cubes = load_cubes(get_test_file_path("samples/d22/huge.txt"))
        self.assertEqual(474140, count_points(cubes))
        pass

    def test_count_all_huge_cubes(self):
        cubes = load_cubes(get_test_file_path("samples/d22/huge.txt"))
        self.assertEqual(2758514936282235, count_all_points(cubes))


class CubeVolume(TestCase):
    def test_single_cube(self):
        ref_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        self.assertEqual(27, get_volume_cube(ref_cube))

    def test_single_hole(self):
        on_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        hole_cube = parse_cube_defn("off x=10..12,y=10..12,z=10..12")
        holed_cube = make_hole(on_cube, hole_cube)
        self.assertEqual(19, get_volume_cube(holed_cube))

    def test_merge_on_cubes(self):
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        first, second = merge_cubes(first_cube, second_cube)
        self.assertEqual(get_volume_cube(first), 27)
        self.assertEqual(get_volume_cube(second), 19)
        self.assertEqual(get_volume_cube(first), 27)
        self.assertEqual(get_volume_cube(second), 19)
        self.assertEqual(get_total_volume([first, second]), 46)

    def test_blackout(self):
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("off x=10..12,y=10..12,z=10..12")
        first, second = merge_cubes(first_cube, second_cube)
        self.assertEqual(get_volume_cube(first), 0)
        self.assertEqual(get_volume_cube(second), 27)

    def test_merge_off_cube(self):
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        off_cube = parse_cube_defn("off x=9..11,y=9..11,z=9..11")
        first, second = merge_cubes(first_cube, second_cube)
        self.assertEqual(get_volume_cube(first), 27)
        self.assertEqual(get_volume_cube(second), 19)
        self.assertEqual(get_total_volume([first, second]), 46)
        first, _ = merge_cubes(first, off_cube)
        self.assertEqual(get_volume_cube(first), 19)
        second, _ = merge_cubes(second, off_cube)
        self.assertEqual(get_volume_cube(second), 19)
        self.assertEqual(get_total_volume([first, second]), 38)


class ConsolidateCubes(TestCase):
    def test_empty_list_off(self):
        cube_list = []
        off_cube = parse_cube_defn("off x=10..12,y=10..12,z=10..12")
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 0)

    def test_empty_list_on(self):
        cube_list = []
        on_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        cube_list = consolidate_cubes(cube_list, on_cube)
        self.assertEqual(get_total_volume(cube_list), 27)

    def test_duplicate_cube(self):
        cube_list = []
        on_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        cube_list = consolidate_cubes(cube_list, on_cube)
        cube_list = consolidate_cubes(cube_list, second_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        self.assertEqual(len(cube_list), 1)

    def test_switch_off(self):
        cube_list = []
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        off_cube = parse_cube_defn("off x=9..11,y=9..11,z=9..11")
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, second_cube)
        self.assertEqual(get_total_volume(cube_list), 46)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 38)

    def test_switch_on_again(self):
        cube_list = []
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        off_cube = parse_cube_defn("off x=9..11,y=9..11,z=9..11")
        fourth_cube = parse_cube_defn("on x=10..10,y=10..10,z=10..10")
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, second_cube)
        self.assertEqual(get_total_volume(cube_list), 46)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 38)
        cube_list = consolidate_cubes(cube_list, fourth_cube)
        self.assertEqual(get_total_volume(cube_list), 39)

    def test_engulf_on(self):
        cube_list = []
        first_cube = parse_cube_defn("on x=10..12,y=10..12,z=10..12")
        second_cube = parse_cube_defn("on x=11..13,y=11..13,z=11..13")
        off_cube = parse_cube_defn("off x=9..11,y=9..11,z=9..11")
        fourth_cube = parse_cube_defn("on x=10..10,y=10..10,z=10..10")
        outter = parse_cube_defn("on x=-1..15,y=-1..15,z=-1..15")
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, second_cube)
        self.assertEqual(get_total_volume(cube_list), 46)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 38)
        cube_list = consolidate_cubes(cube_list, fourth_cube)
        self.assertEqual(get_total_volume(cube_list), 39)
        cube_list = consolidate_cubes(cube_list, outter)
        self.assertEqual(1, len(cube_list))
        self.assertEqual(get_total_volume(cube_list), 17*17*17)

    def test_engulfed_on(self):
        cube_list = []
        first_cube = parse_cube_defn("on x=0..2,y=0..2,z=0..2")
        unit_cube = parse_cube_defn("on x=1..1,y=1..1,z=1..1")
        off_cube = parse_cube_defn("off x=0..1,y=0..1,z=0..1")
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 19)
        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 20)
        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 20)
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 19)

    def test_distinct(self):
        cube_list = []
        first_cube = parse_cube_defn("on x=0..2,y=0..2,z=0..2")
        second_cube = parse_cube_defn("on x=3..4,y=3..4,z=3..4")
        unit_cube = parse_cube_defn("on x=1..1,y=1..1,z=1..1")
        off_cube = parse_cube_defn("off x=0..1,y=0..1,z=0..1")

        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27)

        cube_list = consolidate_cubes(cube_list, second_cube)
        self.assertEqual(get_total_volume(cube_list), 27 + 8)

        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 27 + 8)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 19 + 8)
        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 20 + 8)
        cube_list = consolidate_cubes(cube_list, unit_cube)
        self.assertEqual(get_total_volume(cube_list), 20 + 8)
        cube_list = consolidate_cubes(cube_list, first_cube)
        self.assertEqual(get_total_volume(cube_list), 27 + 8)
        cube_list = consolidate_cubes(cube_list, off_cube)
        self.assertEqual(get_total_volume(cube_list), 19 + 8)
