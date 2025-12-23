from unittest import TestCase

from tools.string_operations import count_chars, subdivide


class TestLoadCharCount(TestCase):
    def test_emptyString(self):
        count = {}
        expected = {}
        count_chars("", count)
        self.assertDictEqual(count, expected)

    def test_singleChar(self):
        count = {}
        expected = {
            "a": 1
        }
        count_chars("a", count)
        self.assertDictEqual(count, expected)

    def test_ManyChars(self):
        count = {}
        expected = {
            "a": 3,
            "b": 4,
            "c": 4,
            "d": 4,
            "e": 2,
            "f": 2
        }
        count_chars("aabbccddeeffddccbba", count)
        self.assertDictEqual(count, expected)


class TestSubdivide(TestCase):
    def test_even_subdivision(self):
        s = "abcdef"
        n = 2
        expected = ["ab", "cd", "ef"]
        self.assertEqual(subdivide(s, n), expected)

    def test_single_char_groups(self):
        s = "abc"
        n = 1
        expected = ["a", "b", "c"]
        self.assertEqual(subdivide(s, n), expected)

    def test_full_string_group(self):
        s = "abcdef"
        n = 6
        expected = ["abcdef"]
        self.assertEqual(subdivide(s, n), expected)

    def test_invalid_factor(self):
        s = "abcde"
        n = 2
        with self.assertRaises(ValueError):
            subdivide(s, n)
