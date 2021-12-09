from unittest import TestCase

from aoc2021.d08 import load_signal_sets, map_signals, part_one
from aoc2021.d08 import get_value, part_two
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class SignalSets(TestCase):
    def test_map_state(self):
        signals = load_signal_sets(get_test_file_path("samples/d08.txt"))
        self.assertEqual(len(signals), 10)
        self.assertListEqual(signals[0].signals, ["be", "cfbegad", "cbdgef", "fgaecd", "cgeb", "fdcge", "agebfd", "fecdb", "fabcd", "edb"])
        self.assertListEqual(signals[0].display,["fdgacbe", "cefdb", "cefbgd", "gcbe"])
        self.assertListEqual(signals[9].signals ,["gcafb", "gcf", "dcaebfg", "ecagb", "gf", "abcdeg", "gaef", "cafbge", "fdbac", "fegbdc"])
        self.assertListEqual(signals[9].display,["fgae", "cfgab", "fg", "bagce"])

    def test_simple_maps(self):
        signal_map =\
            map_signals(["be", "cfbegad", "cbdgef", "fgaecd", "cgeb", "fdcge", "agebfd", "fecdb", "fabcd", "edb"])
        self.assertEqual(signal_map["be"], 1)
        self.assertEqual(signal_map["bde"], 7)
        self.assertEqual(signal_map["bceg"], 4)
        self.assertEqual(signal_map["abcdefg"], 8)

    def test_example_map(self):
        signal_map = \
            map_signals(["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"])
        self.assertEqual(signal_map["ab"], 1)
        self.assertEqual(signal_map["abd"], 7)
        self.assertEqual(signal_map["abef"], 4)
        self.assertEqual(signal_map["abcdefg"], 8)
        self.assertEqual(signal_map["abcdf"], 3)
        self.assertEqual(signal_map["acdfg"], 2)
        self.assertEqual(signal_map["bcdef"], 5)
        self.assertEqual(signal_map["abcdef"], 9)
        self.assertEqual(signal_map["abcdeg"], 0)
        self.assertEqual(signal_map["bcdefg"], 6)


    def test_part_one(self):
        signals = load_signal_sets(get_test_file_path("samples/d08.txt"))
        self.assertEqual(part_one(signals), 26)

    def test_part_two(self):
        signals = load_signal_sets(get_test_file_path("samples/d08.txt"))
        self.assertEqual(part_two(signals), 61229)

    def test_get_values(self):
        signals = load_signal_sets(get_test_file_path("samples/d08.txt"))
        self.assertEqual(get_value(signals[0]), 8394)
        self.assertEqual(get_value(signals[1]), 9781)
        self.assertEqual(get_value(signals[2]), 1197)
        self.assertEqual(get_value(signals[3]), 9361)
        self.assertEqual(get_value(signals[4]), 4873)
        self.assertEqual(get_value(signals[5]), 8418)
        self.assertEqual(get_value(signals[6]), 4548)
        self.assertEqual(get_value(signals[7]), 1625)
        self.assertEqual(get_value(signals[8]), 8717)
        self.assertEqual(get_value(signals[9]), 4315)





