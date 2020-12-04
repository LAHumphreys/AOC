from unittest import TestCase

from aoc2020.d02 import splitRegex
from tests.toolsTests.tools_common import GetTestFilePath
from tools.fileLoader import load_ints, load_int_list, load_lists, load_patterns, load_dicts


class TestLoadInts(TestCase):
    def test_load_ints(self):
        ints = load_ints(GetTestFilePath("input/ints/123"))
        self.assertListEqual(ints, [1, 2, 3])

    def test_load_biggerInts(self):
        ints = load_ints(GetTestFilePath("input/ints/biggerInts"))
        self.assertListEqual(
            ints, [
                50962, 126857, 127476, 136169, 62054, 116866, 123235])

    def test_load_negativeInts(self):
        ints = load_ints(GetTestFilePath("input/ints/negativeInts"))
        self.assertListEqual(
            ints, [
                50962, 126857, -127476, 136169, -62054, 116866, 123235])

    def test_detect_floats(self):
        with self.assertRaises(ValueError) as context:
            load_ints(GetTestFilePath("input/ints/hasFloat"))


class TestLoadIntList(TestCase):
    def test_load_ints(self):
        ints = load_int_list(GetTestFilePath("input/intLIst/123"))
        self.assertListEqual(ints, [1, 2, 3])

    def test_load_biggerInts(self):
        ints = load_int_list(GetTestFilePath("input/intLIst/biggerInts"))
        self.assertListEqual(
            ints, [
                50962, 126857, 127476, 136169, 62054, 116866, 123235])

    def test_load_negativeInts(self):
        ints = load_int_list(GetTestFilePath("input/intLIst/negativeInts"))
        self.assertListEqual(
            ints, [
                50962, 126857, -127476, 136169, -62054, 116866, 123235])

    def test_detect_floats(self):
        with self.assertRaises(ValueError) as context:
            load_int_list(GetTestFilePath("input/intLIst/hasFloat"))


class TestLoadLists(TestCase):
    def test_load_ints(self):
        ints = load_lists(GetTestFilePath("input/lists/123456"))
        self.assertListEqual(ints[0], ["1", "2", "3"])
        self.assertListEqual(ints[1], ["4", "5", "6"])

    def test_load_mix(self):
        ints = load_lists(GetTestFilePath("input/lists/abcdef1234"))
        self.assertListEqual(ints[0], ["a", "b", "c", "d"])
        self.assertListEqual(ints[1], ["e1", "f2"])
        self.assertListEqual(ints[2], ["1", "2", "3", "4"])


class TestLoadPaterns(TestCase):
    def test_load_valid(self):
        groups = load_patterns(splitRegex, GetTestFilePath(
            "input/patterns/validPatterns.txt"))
        expected = [
            ("1", "3", "a", "abcde"),
            ("1", "3", "b", "cdefg"),
            ("2", "9", "c", "ccccccccc")
        ]
        self.assertListEqual(groups, expected)

    def test_load_invalidLine(self):
        with self.assertRaises(ValueError) as context:
            load_patterns(splitRegex, GetTestFilePath(
                "input/patterns/invalidLine"))


class TestLoadDicts(TestCase):
    def test_Example(self):
        dicts = [{"ecl": "gry",
                  "pid": "860033327",
                  "eyr": "2020",
                  "hcl": "#fffffd",
                  "byr": "1937",
                  "iyr": "2017",
                  "cid": "147",
                  "hgt": "183cm",
                  },
                 {"iyr": "2013",
                  "ecl": "amb",
                  "cid": "350",
                  "eyr": "2023",
                  "pid": "028048884",
                  "hcl": "#cfa07d",
                  "byr": "1929",
                  },
                 {"hcl": "#ae17e1",
                  "iyr": "2013",
                  "eyr": "2024",
                  "ecl": "brn",
                  "pid": "760753108",
                  "byr": "1931",
                  "hgt": "179cm",
                  },
                 {"hcl": "#cfa07d",
                  "eyr": "2025",
                  "pid": "166559648",
                  "iyr": "2011",
                  "ecl": "brn",
                  "hgt": "59in",
                  }]
        self.assertListEqual(
            dicts, load_dicts(
                GetTestFilePath("input/dicts/exampleDict")))
