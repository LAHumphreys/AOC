from unittest import TestCase
from aoc2019.d04 import validValue, validValue2

class TestValidValue(TestCase):
    def test_InvalidSample_decreasingDigit(self):
        self.assertFalse(validValue([2,2,3,4,5,0]))

    def test_InvalidSample_NoDouble(self):
        self.assertFalse(validValue([1,2,3,7,8,9]))

    def test_ValidSample_SingleDigit(self):
        self.assertTrue(validValue([1,1,1,1,1,1]))

    def test_ValidSample_AdjacentDigits(self):
        self.assertTrue(validValue([1,2,2,4,5,6]))

    def test_ValidSample_Ascending(self):
        self.assertTrue(validValue([1,1,1,1,2,3]))

class TestValidValue_Part2(TestCase):
    def test_InvalidSample_decreasingDigit(self):
        self.assertFalse(validValue2([2,2,3,4,5,0]))

    def test_InvalidSample_NoDouble(self):
        self.assertFalse(validValue2([1,2,3,7,8,9]))

    def test_Invalid_SingleDigit(self):
        self.assertFalse(validValue2([1,1,1,1,1,1]))

    def test_ValidSample_Pairs(self):
        self.assertTrue(validValue2([1,1,2,2,3,3]))

    def test_InvalidSample_Triplet(self):
        self.assertFalse(validValue2([1,2,3,4,4,4]))

    def test_ValidSample_PairAndQuad(self):
        self.assertTrue(validValue2([1,1,1,1,2,2]))
