from unittest import TestCase

from aoc2023.d19 import parse_rule, Condition, parse_part, load_input
from aoc2023.d19 import is_part_accepted, part_one
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestInput(TestCase):
    def test_parts(self):
        parts = load_input(get_test_file_path("samples/d19.txt")).parts
        self.assertEqual(parts[3].vars, {"x": 2461, "m": 1339, "a": 466, "s": 291})
        self.assertEqual(parts[-1].vars, {"x": 2127, "a": 2188, "m": 1623, "s": 1013})

    def test_rules(self):
        rules = load_input(get_test_file_path("samples/d19.txt")).rules
        self.assertEqual(rules["in"].name, "in")
        self.assertEqual(rules["in"].fallback, "qqz")
        self.assertEqual(rules["in"].conditions[0].variable, "s")
        self.assertEqual(rules["in"].conditions[0].max_value, 1351)
        self.assertEqual(rules["in"].conditions[0].min_value, None)




class TestVarParser(TestCase):
    def test_part(self):
        part = parse_part("{x=2461,m=1339,a=466,s=291}")
        expected = {"x": 2461, "m": 1339, "a": 466, "s": 291}
        self.assertEqual(part.vars, expected)


class TestRuleParser(TestCase):
    def test_name(self):
        rule = parse_rule("px{a<2006:qkq,m>2090:A,rfg}")
        self.assertEqual(rule.name, "px")

    def test_fallback(self):
        rule = parse_rule("px{a<2006:qkq,m>2090:A,rfg}")
        self.assertEqual(rule.fallback, "rfg")

    def test_conditions(self):
        rule = parse_rule("px{a<2006:qkq,m>2090:A,rfg}")
        expected = [
            Condition(variable="a", destination="qkq", min_value=None, max_value=2006),
            Condition(variable="m", destination="A", min_value=2090, max_value=None),
        ]
        self.assertEqual(rule.conditions, expected)


class TestAccepted(TestCase):
    def test_part_one(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(is_part_accepted(input.parts[0], input.rules), True)

    def test_part_two(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(is_part_accepted(input.parts[1], input.rules), False)

    def test_part_three(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(is_part_accepted(input.parts[2], input.rules), True)

    def test_parte_four(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(is_part_accepted(input.parts[3], input.rules), False)

    def test_part_five(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(is_part_accepted(input.parts[4], input.rules), True)

    def test_example(self):
        input = (load_input(get_test_file_path("samples/d19.txt")))
        self.assertEqual(part_one(input), 19114)
