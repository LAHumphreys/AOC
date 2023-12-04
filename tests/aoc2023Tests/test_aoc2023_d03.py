from unittest import TestCase

from aoc2023.d03 import map_row, is_symbol, get_parts, PartNumber, load_blue_print
from aoc2023.d03 import is_valid_part, part_one, Gear, get_ratios, part_two
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestCount(TestCase):
    def test_is_symbol(self):
        self.assertEqual(is_symbol("*"), True)
        self.assertEqual(is_symbol("#"), True)
        self.assertEqual(is_symbol("."), False)
        self.assertEqual(is_symbol("4"), False)
        self.assertEqual(is_symbol("0"), False)
        self.assertEqual(is_symbol("9"), False)

    def test_map_single_row(self):
        self.assertListEqual(map_row("...*......"), [False]*2+[True]*3+[False]*5)
        self.assertListEqual(map_row("#..*.....#"), [True]*2+[True]*3+[False]*3+[True]*2)

    def test_get_part_number_none(self):
        self.assertListEqual(get_parts("...*......"), [])

    def test_get_part_number_single_digit(self):
        expected = [PartNumber(value=7, start_idx=10, end_idx=10)]
        #                               01234567890
        self.assertListEqual(get_parts("..........7...."), expected)

    def test_get_part_number_values(self):
        expected = [PartNumber(value=467, start_idx=0, end_idx=2),
                    PartNumber(value=114, start_idx=5, end_idx=7),
                    PartNumber(value=7, start_idx=10, end_idx=10),
                    PartNumber(value=81, start_idx=13, end_idx=14),
                    ]
        #                               012345678901234
        self.assertListEqual(get_parts("467..114..7..81"), expected)

    def test_load_len(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertEqual(blue_print.max_x, 9)

    def test_load_gears(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        expected = [
            Gear(x=3, y=1), Gear(x=3, y=4), Gear(x=5, y=8)
        ]
        self.assertListEqual(blue_print.gears, expected)

    def test_get_ratios(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertListEqual(get_ratios(blue_print, blue_print.gears[0]), [467, 35])
        self.assertListEqual(get_ratios(blue_print, blue_print.gears[1]), [617])
        self.assertListEqual(get_ratios(blue_print, blue_print.gears[2]), [755, 598])

    def test_load_parts(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        expected = [
            PartNumber(value=467, start_idx=0, end_idx=2),
            PartNumber(value=114, start_idx=5, end_idx=7),
        ]
        self.assertEqual(blue_print.part_numbers[0], expected)
        expected = []
        self.assertEqual(blue_print.part_numbers[1], expected)
        expected = [
            PartNumber(value=58, start_idx=7, end_idx=8),
        ]
        self.assertEqual(blue_print.part_numbers[5], expected)
        expected = [
            PartNumber(value=664, start_idx=1, end_idx=3),
            PartNumber(value=598, start_idx=5, end_idx=7),
        ]
        self.assertEqual(blue_print.part_numbers[9], expected)

    def test_load_row_map(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertListEqual(blue_print.row_maps[1], [False]*2+[True]*3+[False]*5)
        self.assertListEqual(blue_print.row_maps[0], [False]*10)

    def test_valid_parts(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertFalse(is_valid_part(5, 5, 0, blue_print))
        # Same Row
        self.assertTrue(is_valid_part(3, 3, 1, blue_print))
        # Same Below
        self.assertTrue(is_valid_part(3, 3, 0, blue_print))
        # Same After
        self.assertTrue(is_valid_part(3, 3, 2, blue_print))

    def test_part_one(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertEqual(part_one(blue_print), 4361)

    def test_part_two(self):
        blue_print = load_blue_print(get_test_file_path("samples/d03.txt"))
        self.assertEqual(part_two(blue_print), 467835)
