import copy

from unittest import TestCase
from aoc2019.d02 import Compute, Add, Mul, Fixup1202, GravAssistCalc, EncodeAnswer, FindVerbNoun, FindAndEncode

class TestCompute(TestCase):
    def test_Compute_Example1(self):
        self.assertListEqual(Compute([1,0,0,0,99]), [2,0,0,0,99])

    def test_Compute_Example2(self):
        self.assertListEqual(Compute([2,3,0,3,99]), [2,3,0,6,99])

    def test_Compute_Example3(self):
        self.assertListEqual(Compute([2,4,4,5,99,0]), [2,4,4,5,99,9801])

    def test_Compute_Example4(self):
        self.assertListEqual(Compute([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99])

    def test_Compute_EarlyStop(self):
        self.assertListEqual(Compute([1,1,1,5,99,5,6,0,99]), [1,1,1,5,99,2,6,0,99])

class TestFixup(TestCase):
    def test_Fixup_simple(self):
        prog = [99,99,99,99]
        Fixup1202(prog)
        self.assertListEqual(prog, [99,12,2,99])

class TestAdd(TestCase):
    def test_Compute_Example1(self):
        input = [1,0,0,0,99]
        Add(input, 0)
        self.assertListEqual(input, [2,0,0,0,99])

class TestMul(TestCase):
    def test_Compute_Example1(self):
        input = [2,3,0,3,99]
        Mul(input, 0)
        self.assertListEqual(input, [2,3,0,6,99])


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
