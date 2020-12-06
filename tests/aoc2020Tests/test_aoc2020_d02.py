from unittest import TestCase

from aoc2020.d02 import SPLIT_REGEX, is_pass_valid, is_pass_valid_part_2


class TestProduct(TestCase):
    def test_SplitRegex_expected(self):
        m = SPLIT_REGEX.search("1-3 a: abcde")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "1")
        self.assertEqual(m.group(2), "3")
        self.assertEqual(m.group(3), "a")
        self.assertEqual(m.group(4), "abcde")

    def test_SplitRegex_NoCaps(self):
        m = SPLIT_REGEX.search("1-3 a: abCde")
        self.assertIsNone(m)

        m = SPLIT_REGEX.search("1-3 D: abcde")
        self.assertIsNone(m)

    def test_SplitRegex_NoSpaces(self):
        m = SPLIT_REGEX.search("1-3 a: ab de")
        self.assertIsNone(m)


class TestPasswdValid(TestCase):
    def test_Example1(self):
        groups = SPLIT_REGEX.search("1-3 a: abcde").groups()
        self.assertEqual(is_pass_valid(groups), True)

    def test_Example2(self):
        groups = SPLIT_REGEX.search("1-3 b: cdefg").groups()
        self.assertEqual(is_pass_valid(groups), False)

    def test_Example3(self):
        groups = SPLIT_REGEX.search("2-9 c: ccccccccc").groups()
        self.assertEqual(is_pass_valid(groups), True)

    def test_TooFew(self):
        groups = SPLIT_REGEX.search("2-9 d: ccccdcccc").groups()
        self.assertEqual(is_pass_valid(groups), False)

    def test_TooMany(self):
        groups = SPLIT_REGEX.search("2-3 d: ccccddddcccc").groups()
        self.assertEqual(is_pass_valid(groups), False)


class TestPasswdValid_Mode2(TestCase):
    def test_TooShort(self):
        groups = SPLIT_REGEX.search("1-5 a: abc").groups()
        self.assertEqual(is_pass_valid_part_2(groups), False)

    def test_Example1(self):
        groups = SPLIT_REGEX.search("1-3 a: abcde").groups()
        self.assertEqual(is_pass_valid_part_2(groups), True)

    def test_Example2(self):
        groups = SPLIT_REGEX.search("1-3 b: cdefg").groups()
        self.assertEqual(is_pass_valid_part_2(groups), False)

    def test_Example3(self):
        groups = SPLIT_REGEX.search("2-9 c: ccccccccc").groups()
        self.assertEqual(is_pass_valid_part_2(groups), False)
