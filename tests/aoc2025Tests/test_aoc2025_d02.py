from unittest import TestCase
from aoc2025.d02 import load_sample, get_next_repeat, get_invalid_ids, part1
from aoc2025.d02 import  get_invalid_ids_part_2,  part2, get_next_repeat_part_2, is_invalid_part_2, is_invalid
from tests.aoc2025Tests.aoc2025_common import get_test_file_path

class TestDay02(TestCase):
    def setUp(self):
        self.sample_path = get_test_file_path("samples/d02.txt")
        self.lines = load_sample(self.sample_path)

    def test_simple_next(self):
        self.assertEqual(get_next_repeat("10"), "11")
        self.assertEqual(get_next_repeat("11"), "22")
        self.assertEqual(get_next_repeat("95"), "99")
        self.assertEqual(get_next_repeat("998"), "1010")
        self.assertEqual(get_next_repeat("222220"), "222222")
        self.assertEqual(get_next_repeat("1188511880"), "1188511885")

    def test_simple_next_part_2(self):
        self.assertEqual(get_next_repeat_part_2("10"), "11")
        self.assertEqual(get_next_repeat_part_2("11"), "22")
        self.assertEqual(get_next_repeat_part_2("95"), "99")
        self.assertEqual(get_next_repeat_part_2("99"), "111")
        self.assertEqual(get_next_repeat_part_2("998"), "999")
        self.assertEqual(get_next_repeat_part_2("222220"), "222222")
        self.assertEqual(get_next_repeat_part_2("1188511880"), "1188511885")
        self.assertEqual(get_next_repeat_part_2("824824821"), "824824824")
        self.assertEqual(get_next_repeat_part_2("2121212118"), "2121212121")

    def test_invalid_ids(self):
        self.assertEqual(get_invalid_ids("11", "22"), [11, 22])
        self.assertEqual(get_invalid_ids("95", "115"), [99])
        self.assertEqual(get_invalid_ids("998", "1012"), [1010])
        self.assertEqual(get_invalid_ids("1188511880", "1188511890"), [1188511885])

    def test_invalid_ids_part_2(self):
        self.assertEqual(get_invalid_ids_part_2("11", "22"), [11, 22])
        self.assertEqual(get_invalid_ids_part_2("95", "115"), [99, 111])
        self.assertEqual(get_invalid_ids_part_2("998", "1012"), [999, 1010])
        self.assertEqual(get_invalid_ids_part_2("1188511880", "1188511890"), [1188511885])
        self.assertEqual(get_invalid_ids_part_2("222220", "222224"), [222222])
        self.assertEqual(get_invalid_ids_part_2("1698522", "1698528"), [])
        self.assertEqual(get_invalid_ids_part_2("446443", "446449"), [446446])
        self.assertEqual(get_invalid_ids_part_2("38593856", "38593862"), [38593859])
        self.assertEqual(get_invalid_ids_part_2("565653", "565659"), [565656])
        self.assertEqual(get_invalid_ids_part_2("824824821", "824824827"), [824824824])
        self.assertEqual(get_invalid_ids_part_2("2121212118", "2121212124"), [2121212121])

    def test_invalid_is_invalid(self):
        self.assertEqual(is_invalid("99"), True)
        self.assertEqual(is_invalid("99", 1), True)
        self.assertEqual(is_invalid_part_2("99"), True)
        self.assertEqual(is_invalid("111"), False)
        self.assertEqual(is_invalid("111", 1), True)
        self.assertEqual(is_invalid_part_2("111"), True)


    def test_part_one(self):
        self.assertEqual(part1(self.lines), 1227775554)

    def test_part_two(self):
        self.assertEqual(part2(self.lines), 4174379265)
