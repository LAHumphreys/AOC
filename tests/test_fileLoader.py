from unittest import TestCase
from tools.fileLoader import LoadInts, LoadIntList


class TestLoadInts(TestCase):
    def test_load_ints(self):
        ints = LoadInts("input/ints/123")
        self.assertListEqual(ints, [1, 2, 3])

    def test_load_biggerInts(self):
        ints = LoadInts("input/ints/biggerInts")
        self.assertListEqual(ints, [50962, 126857, 127476, 136169, 62054, 116866, 123235])

    def test_load_negativeInts(self):
        ints = LoadInts("input/ints/negativeInts")
        self.assertListEqual(ints, [50962, 126857, -127476, 136169, -62054, 116866, 123235])

    def test_detect_floats(self):
        with self.assertRaises(ValueError) as context:
            LoadInts("input/ints/hasFloat")


class TestLoadIntList(TestCase):
    def test_load_ints(self):
        ints = LoadIntList("input/intLIst/123")
        self.assertListEqual(ints, [1, 2, 3])

    def test_load_biggerInts(self):
        ints = LoadIntList("input/intLIst/biggerInts")
        self.assertListEqual(ints, [50962, 126857, 127476, 136169, 62054, 116866, 123235])

    def test_load_negativeInts(self):
        ints = LoadIntList("input/intLIst/negativeInts")
        self.assertListEqual(ints, [50962, 126857, -127476, 136169, -62054, 116866, 123235])

    def test_detect_floats(self):
        with self.assertRaises(ValueError) as context:
            LoadIntList("input/intLIst/hasFloat")
