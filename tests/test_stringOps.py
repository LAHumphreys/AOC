from unittest import TestCase
from tools.stringsOps import countChars

class TestLoadCharCount(TestCase):
    def test_emptyString(self):
        count = {}
        expected = {}
        countChars("", count)
        self.assertDictEqual(count, expected)

    def test_singleChar(self):
        count = {}
        expected = {
            "a": 1
        }
        countChars("a", count)
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
        countChars("aabbccddeeffddccbba", count)
        self.assertDictEqual(count, expected)
