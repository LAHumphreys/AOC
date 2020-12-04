from unittest import TestCase

from aoc2019.d02 import fixup_1202, GravAssistCalc, encode_answer, find_verb_noun, find_and_encode


class TestFixup(TestCase):
    def test_Fixup_simple(self):
        prog = [99, 99, 99, 99]
        fixup_1202(prog)
        self.assertListEqual(prog, [99, 12, 2, 99])


class TestGravAssist(TestCase):
    def test_Compute_GravAssist_Prob1(self):
        self.calc = GravAssistCalc()
        self.assertEqual(self.calc.compute(12, 2), 4930687)


class TestGravAssistEncode(TestCase):
    def test_Encode_Example(self):
        self.assertEqual(encode_answer(12, 2), 1202)


class TestGravAssistSearch(TestCase):
    def test_Search_Example(self):
        [verb, noun] = find_verb_noun(4930687)
        self.assertEqual(noun, 12)
        self.assertEqual(verb, 2)

    def test_Search_EncodeExample(self):
        self.assertEqual(find_and_encode(4930687), 1202)
