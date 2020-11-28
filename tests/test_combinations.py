from unittest import TestCase
from tools.combinations import Generate, GenerateAscending, MinValueMismatch


class TestGenerate_Simple(TestCase):
   def test_ZeroLen(self):
       self.assertListEqual(Generate(0, [1,2,3]), [])

   def test_SingleDigit(self):
       self.assertListEqual(Generate(1, [1,2,3]), [[1], [2], [3]])

   def test_DoubleDigit(self):
       expected = [
           [1, 1],
           [1, 2],
           [1, 3],
           [2, 1],
           [2, 2],
           [2, 3],
           [3, 1],
           [3, 2],
           [3, 3]
       ]
       self.assertListEqual(Generate(2, [1,2,3]), expected)

   def test_TrippleDigit(self):
       expected = [
           [1, 1, 1],
           [1, 1, 2],
           [1, 1, 3],
           [1, 2, 1],
           [1, 2, 2],
           [1, 2, 3],
           [1, 3, 1],
           [1, 3, 2],
           [1, 3, 3],

           [2, 1, 1],
           [2, 1, 2],
           [2, 1, 3],
           [2, 2, 1],
           [2, 2, 2],
           [2, 2, 3],
           [2, 3, 1],
           [2, 3, 2],
           [2, 3, 3],

           [3, 1, 1],
           [3, 1, 2],
           [3, 1, 3],
           [3, 2, 1],
           [3, 2, 2],
           [3, 2, 3],
           [3, 3, 1],
           [3, 3, 2],
           [3, 3, 3],
       ]
       self.assertListEqual(Generate(3, [1,2,3]), expected)

   def test_QuadrupleDigit(self):
       expected = [
           [1, 1, 1, 1],
           [1, 1, 1, 2],
           [1, 1, 1, 3],
           [1, 1, 2, 1],
           [1, 1, 2, 2],
           [1, 1, 2, 3],
           [1, 1, 3, 1],
           [1, 1, 3, 2],
           [1, 1, 3, 3],
           [1, 2, 1, 1],
           [1, 2, 1, 2],
           [1, 2, 1, 3],
           [1, 2, 2, 1],
           [1, 2, 2, 2],
           [1, 2, 2, 3],
           [1, 2, 3, 1],
           [1, 2, 3, 2],
           [1, 2, 3, 3],
           [1, 3, 1, 1],
           [1, 3, 1, 2],
           [1, 3, 1, 3],
           [1, 3, 2, 1],
           [1, 3, 2, 2],
           [1, 3, 2, 3],
           [1, 3, 3, 1],
           [1, 3, 3, 2],
           [1, 3, 3, 3],

           [2, 1, 1, 1],
           [2, 1, 1, 2],
           [2, 1, 1, 3],
           [2, 1, 2, 1],
           [2, 1, 2, 2],
           [2, 1, 2, 3],
           [2, 1, 3, 1],
           [2, 1, 3, 2],
           [2, 1, 3, 3],
           [2, 2, 1, 1],
           [2, 2, 1, 2],
           [2, 2, 1, 3],
           [2, 2, 2, 1],
           [2, 2, 2, 2],
           [2, 2, 2, 3],
           [2, 2, 3, 1],
           [2, 2, 3, 2],
           [2, 2, 3, 3],
           [2, 3, 1, 1],
           [2, 3, 1, 2],
           [2, 3, 1, 3],
           [2, 3, 2, 1],
           [2, 3, 2, 2],
           [2, 3, 2, 3],
           [2, 3, 3, 1],
           [2, 3, 3, 2],
           [2, 3, 3, 3],

           [3, 1, 1, 1],
           [3, 1, 1, 2],
           [3, 1, 1, 3],
           [3, 1, 2, 1],
           [3, 1, 2, 2],
           [3, 1, 2, 3],
           [3, 1, 3, 1],
           [3, 1, 3, 2],
           [3, 1, 3, 3],
           [3, 2, 1, 1],
           [3, 2, 1, 2],
           [3, 2, 1, 3],
           [3, 2, 2, 1],
           [3, 2, 2, 2],
           [3, 2, 2, 3],
           [3, 2, 3, 1],
           [3, 2, 3, 2],
           [3, 2, 3, 3],
           [3, 3, 1, 1],
           [3, 3, 1, 2],
           [3, 3, 1, 3],
           [3, 3, 2, 1],
           [3, 3, 2, 2],
           [3, 3, 2, 3],
           [3, 3, 3, 1],
           [3, 3, 3, 2],
           [3, 3, 3, 3],
       ]
       self.assertListEqual(Generate(4, [1,2,3]), expected)

class TestGenerate_Repeats(TestCase):
    def test_SingleDigit_CannotRepeat(self):
        self.assertListEqual(Generate(1, [1, 2, 3], consecutiveRepeats=1), [])

    def test_DoubleDigit_CannotDoubleRepeat(self):
        self.assertListEqual(Generate(2, [1, 2, 3], consecutiveRepeats=2), [])

    def test_DoubleDigit_SingleRepeat(self):
        expected = [
            [1, 1],
            [2, 2],
            [3, 3]
        ]
        self.assertListEqual(Generate(2, [1, 2, 3], consecutiveRepeats=1), expected)

    def test_TrippleDigit_CannotTrippleRepeat(self):
        self.assertListEqual(Generate(3, [1, 2, 3], consecutiveRepeats=3), [])

    def test_TrippleDigit_DoubleRepeat(self):
        expected = [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
        ]
        self.assertListEqual(Generate(3, [1, 2, 3], consecutiveRepeats=2), expected)

    def test_TrippleDigit_SingleRepeat(self):
        expected = [
            [1, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
            [1, 2, 2],
            [1, 3, 3],
            [2, 1, 1],
            [2, 2, 1],
            [2, 2, 2],
            [2, 2, 3],
            [2, 3, 3],
            [3, 1, 1],
            [3, 2, 2],
            [3, 3, 1],
            [3, 3, 2],
            [3, 3, 3],

        ]
        self.assertListEqual(Generate(3, [1, 2, 3], consecutiveRepeats=1), expected)

    def test_QuadrupleDigit_CannotQuadrupleRepeat(self):
        self.assertListEqual(Generate(4, [1, 2, 3], consecutiveRepeats=4), [])

    def test_QuadrupleDigit_TrippleRepeat(self):
        expected = [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ]
        self.assertListEqual(Generate(4, [1, 2, 3], consecutiveRepeats=3), expected)

    def test_QuadrupleDigit_DoubleRepeat(self):
        expected = [
            [1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 1, 3],
            [1, 2, 2, 2],
            [1, 3, 3, 3],

            [2, 1, 1, 1],
            [2, 2, 2, 1],
            [2, 2, 2, 2],
            [2, 2, 2, 3],
            [2, 3, 3, 3],

            [3, 1, 1, 1],
            [3, 2, 2, 2],
            [3, 3, 3, 1],
            [3, 3, 3, 2],
            [3, 3, 3, 3],
        ]
        self.assertListEqual(Generate(4, [1, 2, 3], consecutiveRepeats=2), expected)

    def test_QuadrupleDigit_SingleRepeat(self):
        expected = [
            [1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 1, 3],
            [1, 1, 2, 1],
            [1, 1, 2, 2],
            [1, 1, 2, 3],
            [1, 1, 3, 1],
            [1, 1, 3, 2],
            [1, 1, 3, 3],
            [1, 2, 1, 1],
            [1, 2, 2, 1],
            [1, 2, 2, 2],
            [1, 2, 2, 3],
            [1, 2, 3, 3],
            [1, 3, 1, 1],
            [1, 3, 2, 2],
            [1, 3, 3, 1],
            [1, 3, 3, 2],
            [1, 3, 3, 3],

            [2, 1, 1, 1],
            [2, 1, 1, 2],
            [2, 1, 1, 3],
            [2, 1, 2, 2],
            [2, 1, 3, 3],
            [2, 2, 1, 1],
            [2, 2, 1, 2],
            [2, 2, 1, 3],
            [2, 2, 2, 1],
            [2, 2, 2, 2],
            [2, 2, 2, 3],
            [2, 2, 3, 1],
            [2, 2, 3, 2],
            [2, 2, 3, 3],
            [2, 3, 1, 1],
            [2, 3, 2, 2],
            [2, 3, 3, 1],
            [2, 3, 3, 2],
            [2, 3, 3, 3],

            [3, 1, 1, 1],
            [3, 1, 1, 2],
            [3, 1, 1, 3],
            [3, 1, 2, 2],
            [3, 1, 3, 3],
            [3, 2, 1, 1],
            [3, 2, 2, 1],
            [3, 2, 2, 2],
            [3, 2, 2, 3],
            [3, 2, 3, 3],
            [3, 3, 1, 1],
            [3, 3, 1, 2],
            [3, 3, 1, 3],
            [3, 3, 2, 1],
            [3, 3, 2, 2],
            [3, 3, 2, 3],
            [3, 3, 3, 1],
            [3, 3, 3, 2],
            [3, 3, 3, 3],
        ]
        self.assertListEqual(Generate(4, [1, 2, 3], consecutiveRepeats=1), expected)

class TestGenerateAscending_Simple(TestCase):
    def test_ZeroLen(self):
        self.assertListEqual(GenerateAscending(0, [1,2,3]), [])

    def test_SingleDigit(self):
        self.assertListEqual(GenerateAscending(1, [1,2,3]), [[1], [2], [3]])

    def test_DoubleDigit(self):
        expected = [
            [1, 1],
            [1, 2],
            [1, 3],
            [2, 2],
            [2, 3],
            [3, 3]
        ]
        self.assertListEqual(GenerateAscending(2, [1,2,3]), expected)

    def test_TrippleDigit(self):
        expected = [
            [1, 1, 1],
            [1, 1, 2],
            [1, 1, 3],
            [1, 2, 2],
            [1, 2, 3],
            [1, 3, 3],

            [2, 2, 2],
            [2, 2, 3],
            [2, 3, 3],

            [3, 3, 3],
        ]
        self.assertListEqual(GenerateAscending(3, [1,2,3]), expected)

    def test_QuadrupleDigit(self):
        expected = [
            [1, 1, 1, 1],
            [1, 1, 1, 2],
            [1, 1, 1, 3],
            [1, 1, 2, 2],
            [1, 1, 2, 3],
            [1, 1, 3, 3],
            [1, 2, 2, 2],
            [1, 2, 2, 3],
            [1, 2, 3, 3],
            [1, 3, 3, 3],

            [2, 2, 2, 2],
            [2, 2, 2, 3],
            [2, 2, 3, 3],
            [2, 3, 3, 3],

            [3, 3, 3, 3],
        ]
        self.assertListEqual(GenerateAscending(4, [1,2,3]), expected)

class TestGenerateAscending_MinValue(TestCase):

    def test_MinValue_TooShort(self):
        self.assertRaises(MinValueMismatch, lambda : GenerateAscending(4, [1,2,3], minValue=[1,2]))

    def test_MinValue_TooLong(self):
        self.assertRaises(MinValueMismatch, lambda : GenerateAscending(4, [1,2,3], minValue=[1,2,3,4,5]))

