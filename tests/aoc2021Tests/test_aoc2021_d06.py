from unittest import TestCase

from aoc2021.d06 import part_one, map_state, run_model

class TestVectorParsing(TestCase):
    def test_map_state(self):
        self.assertListEqual(map_state([3,4,3,1,2]), [0, 1, 1, 2, 1, 0, 0, 0, 0])

    def test_run_model(self):
        year_1 = run_model([0, 1, 1, 2, 1, 0, 0, 0, 0])
        self.assertListEqual(year_1, [1, 1, 2, 1, 0, 0, 0, 0, 0])

        year_2 = run_model(year_1)
        self.assertListEqual(year_2, [1, 2, 1, 0, 0, 0, 1, 0, 1])

    def test_vector_parse(self):
        self.assertEqual(part_one([3,4,3,1,2], 18), 26)
        self.assertEqual(part_one([3,4,3,1,2], 80), 5934)

