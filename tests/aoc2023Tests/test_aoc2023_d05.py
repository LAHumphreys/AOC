from unittest import TestCase

from aoc2023.d05 import parse_map_range, parse_input, MapRange, Range
from aoc2023.d05 import locate_seed, part_one, apply_map_to_range, MapBlock
from aoc2023.d05 import part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_parse_range(self):
        map_range = parse_map_range("49 53 8")
        self.assertEqual(map_range.offset, -4)
        self.assertEqual(map_range.source_start, 53)
        self.assertEqual(map_range.source_end, 60)

    def test_load_seeds(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        self.assertEqual(instructions.seeds, [79, 14, 55, 13])

    def test_load_seed_pairs(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        self.assertEqual(instructions.seed_ranges,
        [Range(start=79, end=79+ 14), Range(start=55, end=55+13)])

    def test_load_blocks(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        seed_block = instructions.maps["seed"]
        expected = [
            MapRange(source_start=50, source_end=97, offset=2),
            MapRange(source_start=98, source_end=99, offset=-48),
        ]
        self.assertEqual(seed_block.map_to, "soil")
        self.assertEqual(seed_block.ranges, expected)

    def test_locate_seed(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        self.assertEqual(locate_seed(79, instructions), 82)


class TestExamples(TestCase):
    def test_part_one(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        self.assertEqual(part_one(instructions), 35)

    def test_part_two(self):
        instructions = parse_input(get_test_file_path("samples/d05.txt"))
        self.assertEqual(part_two(instructions), 46)



class TestBlockMap(TestCase):

    def setUp(self):
        self.block = MapBlock(
            map_to="test",
            ranges=[MapRange(source_start=50, source_end=97, offset=2),
                    MapRange(source_start=98, source_end=99, offset=-48)])

    def test_out_of_range(self):

        self.assertEqual(
            apply_map_to_range(Range(start=101, end=105), self.block),
            [Range(start=101, end=105)])

        self.assertEqual(
            apply_map_to_range(Range(start=25, end=49), self.block),
            [Range(start=25, end=49)])

    def test_inside_block(self):
        self.assertEqual(
            apply_map_to_range(Range(start=75, end=90), self.block),
            [Range(start=77, end=92)])
        pass

    def test_full_range(self):
        self.assertEqual(
            apply_map_to_range(Range(start=0, end=101), self.block), [Range(start=0, end=101)])

    def test_slice_two_blockss(self):
        self.assertEqual(
            apply_map_to_range(Range(start=95, end=98), self.block),
            [Range(start=50, end=50), Range(start=97, end=99)])

