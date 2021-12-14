from unittest import TestCase

from aoc2021.d14 import load_map, apply_expansions, apply_steps, get_score
from aoc2021.d14 import encode_poly, expand_encoded, get_encoded_score, score_steps
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class CorruptDetector(TestCase):

    def test_load_map(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        expected = {
            "CH": "B",
            "HH": "N",
            "CB": "H",
            "NH": "C",
            "HB": "C",
            "HC": "B",
            "HN": "C",
            "NN": "C",
            "BH": "H",
            "NC": "B",
            "NB": "B",
            "BN": "B",
            "BB": "N",
            "BC": "B",
            "CC": "N",
            "CN": "C"
        }
        self.assertDictEqual(expansions, expected)

    def test_expansions(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        self.assertEqual(apply_expansions(expansions, "NNCB"), "NCNBCHB")
        self.assertEqual(apply_expansions(expansions, "NCNBCHB"), "NBCCNBBBCBHCB")
        self.assertEqual(apply_expansions(expansions, "NBCCNBBBCBHCB"), "NBBBCNCCNBBNBNBBCHBHHBCHB")
        self.assertEqual(apply_expansions(expansions, "NBBBCNCCNBBNBNBBCHBHHBCHB"), "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")

    def test_steps(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        self.assertEqual(apply_steps(4, expansions, "NNCB"), "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")

    def test_example(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        expanded = apply_steps(10, expansions, "NNCB")
        self.assertEqual(len(expanded), 3073)
        self.assertEqual(get_score(expanded), 1588)

    def test_encoded_example(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        score = score_steps(10, expansions, "NNCB")
        self.assertEqual(score, 1588)

    def test_encoded_score(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        expanded = apply_steps(10, expansions, "NNCB")
        encoded = encode_poly(expanded)
        self.assertEqual(get_encoded_score(encoded), 1588)

    def test_encode_poly(self):
        expected = { "NN": 1, "NC": 1, "CB": 1, "B\n": 1}
        self.assertDictEqual(encode_poly("NNCB"), expected)

        expected = { "NC": 1, "CN": 1, "NB": 1, "BC": 1, "CH": 1, "HB": 1, "B\n": 1}
        self.assertDictEqual(encode_poly("NCNBCHB"), expected)

        expected = { "AA": 1, "AB": 2, "BC": 2, "CA": 1, "C\n": 1}
        self.assertDictEqual(encode_poly("AABCABC"), expected)

    def test_encoded_expand(self):
        expansions = load_map(get_test_file_path("samples/d14.txt"))
        encoded_poly = encode_poly("NNCB")
        expected = encode_poly("NCNBCHB")
        expanded = expand_encoded(expansions, encoded_poly)
        self.assertDictEqual(expanded, expected)

