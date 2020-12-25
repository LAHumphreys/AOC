from unittest import TestCase

from aoc2020.d19 import parse_ruleset, UnknownRule, parse_input, get_matching_images, patch_rules
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class Validator(TestCase):
    a_b_ruleset = """ 3: 99
    7: 12
    8: 12 4
    9: 12 4 | 4 15
    12: "a"
    4: "b"
    15: "c"
    """

    def test_starts_with_a(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["12"]
        self.assertEqual(rule.matches("aba", rules), (True, "ba"))
        self.assertEqual(rule.matches("bab", rules), (False, ""))
        self.assertEqual(rule.matches("bb", rules), (False, ""))
        self.assertEqual(rule.matches("aa", rules), (True, "a"))

    def test_starts_with_b(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["4"]
        self.assertEqual(rule.matches("bab", rules), (True, "ab"))
        self.assertEqual(rule.matches("aba", rules), (False, ""))
        self.assertEqual(rule.matches("aa", rules), (False, ""))
        self.assertEqual(rule.matches("bb", rules), (True, "b"))

    def test_unknown_rule(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["3"]
        self.assertRaises(UnknownRule, lambda: rule.matches("ababa", rules))

    def test_single_sub_rule(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["7"]
        self.assertEqual(rule.matches("aba", rules), (True, "ba"))
        self.assertEqual(rule.matches("bab", rules), (False, ""))
        self.assertEqual(rule.matches("bb", rules), (False, ""))
        self.assertEqual(rule.matches("aa", rules), (True, "a"))

    def test_multiple_sub_rule(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["8"]
        self.assertEqual(rule.matches("aba", rules), (True, "a"))
        self.assertEqual(rule.matches("bab", rules), (False, ""))
        self.assertEqual(rule.matches("bb", rules), (False, ""))
        self.assertEqual(rule.matches("aa", rules), (False, ""))
        self.assertEqual(rule.matches("ac", rules), (False, ""))

        self.assertEqual(rule.matches("ab", rules), (True, ""))
        self.assertEqual(rule.matches("ba", rules), (False, ""))

    def test_split_sub_rule(self):
        rules = parse_ruleset(self.a_b_ruleset)
        rule = rules["9"]  # ab or bc
        self.assertEqual(rule.matches("aba", rules), (True, "a"))
        self.assertEqual(rule.matches("bab", rules), (False, ""))
        self.assertEqual(rule.matches("bb", rules), (False, ""))
        self.assertEqual(rule.matches("aa", rules), (False, ""))
        self.assertEqual(rule.matches("acc", rules), (False, ""))
        self.assertEqual(rule.matches("bcc", rules), (True, "c"))

        self.assertEqual(rule.matches("ab", rules), (True, ""))
        self.assertEqual(rule.matches("bc", rules), (True, ""))
        self.assertEqual(rule.matches("ba", rules), (False, ""))

        self.assertEqual(rule.matches("aaab", rules), (False, ""))
        self.assertEqual(rule.matches("bbbbc", rules), (False, ""))
        self.assertEqual(rule.matches("bbbba", rules), (False, ""))


class MatchIterator(TestCase):
    def setUp(self):
        self.branching_ruleset = """ 0: 4 1 5
        1: 2 3 | 3 2
        2: 4 4 | 5 5
        3: 4 5 | 5 4
        4: "a"
        5: "b"
        99: 4 | 4 4
        """
        self.rules = parse_ruleset(self.branching_ruleset)
        self.matching_pair_rule = self.rules["2"]
        self.opposite_pair_rule = self.rules["3"]
        self.matching_and_opposite_pairs_rule = self.rules["1"]
        self.a_rule = self.rules["4"]

    def test_fixed_rules_matches(self):
        match_sequence = self.a_rule.get_matches("aba", self.rules)
        self.assertListEqual(list(match_sequence), ["ba"])

    def test_fixed_rules_no_match(self):
        match_sequence = self.a_rule.get_matches("bbb", self.rules)
        self.assertListEqual(list(match_sequence), [])

    def test_ruleset_branching_single_match(self):
        match_sequence = self.matching_pair_rule.get_matches("bbaab", self.rules)
        self.assertListEqual(list(match_sequence), ["aab"])

    def test_ruleset_branching_multi_match(self):
        a_or_double_a = self.rules["99"]
        match_sequence = a_or_double_a.get_matches("aaba", self.rules)
        self.assertListEqual(list(match_sequence), ["aba", "ba"])


class Part1(TestCase):
    def test_example_one(self):
        rules, images = parse_input(GetTestFilePath("samples/d19/sample1.txt"))
        rule_zero = rules["0"]
        self.assertEqual(rule_zero.exactly_matches("ababbb", rules), True)
        self.assertEqual(rule_zero.exactly_matches("abbbab", rules), True)
        self.assertEqual(rule_zero.exactly_matches("bababa", rules), False)
        self.assertEqual(rule_zero.exactly_matches("aaabbb", rules), False)
        self.assertEqual(rule_zero.exactly_matches("aaaabbb", rules), False)

    def test_get_matching_images(self):
        expected = ["ababbb", "abbbab"]
        rules, images = parse_input(GetTestFilePath("samples/d19/sample1.txt"))
        rule_zero = rules["0"]
        self.assertListEqual(expected, get_matching_images(rule_zero, rules, images))


class Part2(TestCase):
    def test_get_matching_images(self):
        expected = ["bbabbbbaabaabba", "ababaaaaaabaaab", "ababaaaaabbbaba"]
        rules, images = parse_input(GetTestFilePath("samples/d19/sample2.txt"))
        rule_zero = rules["0"]
        self.assertListEqual(expected, get_matching_images(rule_zero, rules, images))

    def test_get_patched_matching_images(self):
        expected = ["bbabbbbaabaabba",
                    "babbbbaabbbbbabbbbbbaabaaabaaa",
                    "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
                    "bbbbbbbaaaabbbbaaabbabaaa",
                    "bbbababbbbaaaaaaaabbababaaababaabab",
                    "ababaaaaaabaaab",
                    "ababaaaaabbbaba",
                    "baabbaaaabbaaaababbaababb",
                    "abbbbabbbbaaaababbbbbbaaaababb",
                    "aaaaabbaabaaaaababaa",
                    "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
                    "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"]
        rules, images = parse_input(GetTestFilePath("samples/d19/sample2.txt"))
        patch_rules(rules)
        rule_zero = rules["0"]
        self.assertListEqual(expected, get_matching_images(rule_zero, rules, images))
