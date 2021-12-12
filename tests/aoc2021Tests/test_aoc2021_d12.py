from unittest import TestCase

from aoc2021.d12 import load_map, get_cave_type, CaveType, get_path_options, get_paths
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class CorruptDetector(TestCase):

    def test_load_map(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        self.assertEqual(len(cave_map), 6)
        self.assertListEqual(cave_map["start"], ["A", "b"])
        self.assertListEqual(cave_map["A"], ["start", "c", "b", "end"])
        self.assertListEqual(cave_map["b"], ["start", "A", "d", "end"])
        self.assertListEqual(cave_map["c"], ["A"])
        self.assertListEqual(cave_map["d"], ["b"])
        self.assertListEqual(cave_map["end"], ["A", "b"])

    def test_cave_type(self):
        self.assertEqual(get_cave_type("a"), CaveType.SMALL)
        self.assertEqual(get_cave_type("b"), CaveType.SMALL)
        self.assertEqual(get_cave_type("z"), CaveType.SMALL)

        self.assertEqual(get_cave_type("A"), CaveType.LARGE)
        self.assertEqual(get_cave_type("B"), CaveType.LARGE)
        self.assertEqual(get_cave_type("Z"), CaveType.LARGE)

        self.assertEqual(get_cave_type("start"), CaveType.START)
        self.assertEqual(get_cave_type("end"), CaveType.END)

    def test_cave_type_double(self):
        self.assertEqual(get_cave_type("AA"), CaveType.LARGE)
        self.assertEqual(get_cave_type("AB"), CaveType.LARGE)
        self.assertEqual(get_cave_type("JN"), CaveType.LARGE)
        self.assertEqual(get_cave_type("ZZ"), CaveType.LARGE)

        self.assertEqual(get_cave_type("aa"), CaveType.SMALL)
        self.assertEqual(get_cave_type("ab"), CaveType.SMALL)
        self.assertEqual(get_cave_type("jn"), CaveType.SMALL)
        self.assertEqual(get_cave_type("zz"), CaveType.SMALL)

    def test_get_path_options_start(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        self.assertListEqual(get_path_options(cave_map, ["start"]), ["A", "b"])
        self.assertListEqual(get_path_options(cave_map, ["start"], 2), ["A", "b"])

    def test_get_path_options_end(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        self.assertListEqual(get_path_options(cave_map, ["start", "A", "end"]), [])
        self.assertListEqual(get_path_options(cave_map, ["start", "A", "end"], 2), [])

    def test_get_path_options_simple(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        self.assertListEqual(get_path_options(cave_map, ["start", "b"]), ["A", "d", "end"])
        self.assertListEqual(get_path_options(cave_map, ["start", "A"]), ["c", "b", "end"])
        self.assertListEqual(get_path_options(cave_map, ["start", "b"], 2), ["A", "d", "end"])
        self.assertListEqual(get_path_options(cave_map, ["start", "A"], 2), ["c", "b", "end"])

    def test_get_path_options_revisit(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        self.assertListEqual(get_path_options(cave_map, ["start", "b", "A"]), ["c", "end"])
        self.assertListEqual(get_path_options(cave_map, ["start", "A", "b"]), ["A", "d", "end"])

    def test_get_path_options_revisit_single_small_once(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        # May only visit *one* small cave twice
        self.assertListEqual(get_path_options(cave_map, ["start", "b", "A", "b", "A", "c", "A"], 2), ["end"])

    def test_get_path_options_revisit_small_once(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        # No change to rules on revisiting large caves
        self.assertListEqual(get_path_options(cave_map, ["start", "A", "b"], 2), ["A", "d", "end"])

        # May revisit a singel small cave
        self.assertListEqual(get_path_options(cave_map, ["start", "b", "A"], 2), ["c", "b", "end"])

        # But may not re-visit for a third time
        self.assertListEqual(get_path_options(cave_map, ["start", "b", "A", "b", "A"], 2), ["c", "end"])

    def test_get_small_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        paths = get_paths(cave_map)
        self.assertEqual(len(paths), 10)

    def test_get_small_double_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/small_map.txt"))
        paths = get_paths(cave_map, small_limit=2)
        self.assertEqual(len(paths), 36)

    def test_get_medium_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/medium_map.txt"))
        paths = get_paths(cave_map)
        self.assertEqual(len(paths), 19)

    def test_get_medium_double_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/medium_map.txt"))
        paths = get_paths(cave_map, small_limit=2)
        self.assertEqual(len(paths), 103)

    def test_get_large_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/large.txt"))
        paths = get_paths(cave_map)
        self.assertEqual(len(paths), 226)

    def test_get_large_double_paths(self):
        cave_map = load_map(get_test_file_path("samples/d12/large.txt"))
        paths = get_paths(cave_map, small_limit=2)
        self.assertEqual(len(paths), 3509)
