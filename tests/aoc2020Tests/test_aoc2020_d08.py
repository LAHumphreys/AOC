from unittest import TestCase

from aoc2020.d08 import part_2, load_code, OperationCode, flip_op, repair
from tests.aoc2020Tests.aoc2020_common import GetTestFilePath


class Test_Part1(TestCase):
    def test_load_code(self):
        path = GetTestFilePath("samples/d08/sample1.txt")
        computer = load_code(path)
        self.assertEqual(computer.instruction_pointer, 0)
        self.assertEqual(computer.get_this_operation(), OperationCode.NO_OP)
        computer.execute_until_repeated()
        self.assertEqual(computer.instruction_pointer, 1)
        self.assertEqual(computer.get_this_operation(), OperationCode.ACCUMULATE)
        self.assertEqual(computer.accumulator, 5)

    def test_load_flip(self):
        path = GetTestFilePath("samples/d08/sample1.txt")
        computer = load_code(path)
        computer.code[-2].operation = flip_op(computer.code[-2].operation)
        computer.execute_until_repeated()
        self.assertEqual(computer.instruction_pointer, len(computer.code))

    def test_repair(self):
        path = GetTestFilePath("samples/d08/sample1.txt")
        computer = load_code(path)
        repair(computer)
        self.assertEqual(computer.accumulator, 8)

class Test_Part2(TestCase):
    def test_Example2(self):
        path = GetTestFilePath("samples/d08/sample2.txt")
        expected = "world"
        self.assertEqual(expected, part_2(path))
