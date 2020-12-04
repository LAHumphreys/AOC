from unittest import TestCase

from aoc2020.d01 import find_product, find_trio_product


class TestProduct(TestCase):
    def test_Sample(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(find_product(numbers), 514579)


class TestProductTrio(TestCase):
    def test_Sample(self):
        numbers = [1721, 979, 366, 299, 675, 1456]
        self.assertEqual(find_trio_product(numbers), 241861950)
