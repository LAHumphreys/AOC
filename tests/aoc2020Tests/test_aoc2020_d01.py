from aoc2020.d01 import FindProduct, FindTrioProduct
from unittest import TestCase

class TestProduct(TestCase):
    def test_Sample(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(FindProduct(numbers), 514579)

class TestProductTrio(TestCase):
    def test_Sample(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(FindTrioProduct(numbers), 241861950)
