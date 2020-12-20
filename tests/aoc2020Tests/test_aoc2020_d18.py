from unittest import TestCase

from aoc2020.d18 import stack_calculator, stack_calculator_precedence


class StackCalc(TestCase):
    def test_fix_number(self):
        self.assertEqual(5, stack_calculator("5"))

    def test_simple_add(self):
        self.assertEqual(10, stack_calculator("5 + 5"))

    def test_tripple_add(self):
        self.assertEqual(9, stack_calculator("1 + 2 + 3 + 3"))

    def test_multiple(self):
        self.assertEqual(6, stack_calculator("3 * 2"))

    def test_tripple_multiply(self):
        self.assertEqual(24, stack_calculator("3 * 2 * 4"))

    def test_lhs_precedence(self):
        self.assertEqual(10, stack_calculator("3 * 2 + 4"))
        self.assertEqual(20, stack_calculator("3 + 2 * 4"))

    def test_example_1(self):
        self.assertEqual(71, stack_calculator("1 + 2 * 3 + 4 * 5 + 6"))

    def test_lhs_simple_bracket(self):
        self.assertEqual(20, stack_calculator("3 + 2 * 4"))
        self.assertEqual(11, stack_calculator("3 + (2 * 4)"))

    def test_lhs_double_bracket(self):
        self.assertEqual(3 + 6 + 8 + 5, stack_calculator("3 + (3 * 2) + (2 * 4) + 5"))

    def test_lhs_embeded_bracket(self):
        self.assertEqual(21, stack_calculator("3 + (3 * (2 + 4))"))

    def test_examples(self):
        self.assertEqual(51, stack_calculator("1 + (2 * 3) + (4 * (5 + 6))"))
        self.assertEqual(26, stack_calculator("2 * 3 + (4 * 5)"))
        self.assertEqual(437, stack_calculator("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
        self.assertEqual(12240, stack_calculator("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
        self.assertEqual(13632, stack_calculator("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))


class StackCalcPecedence(TestCase):
    def test_fix_number(self):
        self.assertEqual(5, stack_calculator_precedence("5"))

    def test_simple_add(self):
        self.assertEqual(10, stack_calculator_precedence("5 + 5"))

    def test_tripple_add(self):
        self.assertEqual(9, stack_calculator_precedence("1 + 2 + 3 + 3"))

    def test_multiple(self):
        self.assertEqual(6, stack_calculator_precedence("3 * 2"))

    def test_tripple_multiply(self):
        self.assertEqual(24, stack_calculator_precedence("3 * 2 * 4"))

    def test_precedence(self):
        self.assertEqual(20, stack_calculator_precedence("3 + 2 * 4"))
        self.assertEqual(18, stack_calculator_precedence("3 * 2 + 4"))

    def test_lhs_simple_bracket(self):
        self.assertEqual(11, stack_calculator_precedence("3 + (2 * 4)"))

    def test_lhs_embeded_bracket(self):
        self.assertEqual(21, stack_calculator_precedence("3 + (3 * (2 + 4))"))

    def test_lhs_embeded_bracket_precdence(self):
        self.assertEqual(42, stack_calculator_precedence("2 * 3 + (3 * (2 + 4))"))

    def test_lhs_embeded_bracket_precdence_tail_add(self):
        self.assertEqual(46, stack_calculator_precedence("2 * 3 + (3 * (2 + 4)) + 2"))

    def test_lhs_embeded_bracket_precdence_tail_pair(self):
        self.assertEqual(138, stack_calculator_precedence("2 * 3 + (3 * (2 + 4)) + 2 * 3"))

    def test_lhs_embeded_bracket_multiply(self):
        self.assertEqual(26, stack_calculator_precedence("(3 * 2 + 6) + 2"))

    def test_examples(self):
        self.assertEqual(231, stack_calculator_precedence("1 + 2 * 3 + 4 * 5 + 6"))
        self.assertEqual(51, stack_calculator_precedence("1 + (2 * 3) + (4 * (5 + 6))"))
        self.assertEqual(46, stack_calculator_precedence("2 * 3 + (4 * 5)"))
        self.assertEqual(1445, stack_calculator_precedence("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
        self.assertEqual(669060, stack_calculator_precedence("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
        self.assertEqual(23340, stack_calculator_precedence("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))
