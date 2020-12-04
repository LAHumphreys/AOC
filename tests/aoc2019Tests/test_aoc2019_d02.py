from unittest import TestCase
from aoc2019.d02 import Fixup1202, GravAssistCalc, EncodeAnswer, FindVerbNoun, FindAndEncode


class TestFixup(TestCase):
    def test_Fixup_simple(self):
        prog = [99,99,99,99]
        Fixup1202(prog)
        self.assertListEqual(prog, [99,12,2,99])

class TestGravAssist(TestCase):
    def test_Compute_GravAssist_Prob1(self):
        self.calc = GravAssistCalc()
        self.assertEqual(self.calc.Compute(12, 2), 4930687)

class TestGravAssistEncode(TestCase):
    def test_Encode_Example(self):
        self.assertEqual(EncodeAnswer(12, 2), 1202)


class TestGravAssistSearch(TestCase):
    def test_Search_Example(self):
        [verb, noun] = FindVerbNoun(4930687)
        self.assertEqual(noun, 12)
        self.assertEqual(verb, 2)

    def test_Search_EncodeExample(self):
        self.assertEqual(FindAndEncode(4930687), 1202)
