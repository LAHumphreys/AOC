import copy
import re
from enum import Enum

from tools.file_loader import load_one, load_patterns


class OperationCode(Enum):
    NO_OP = 0
    ACCUMULATE = 1
    JUMP = 2


class UnknownCode(Exception):
    pass


def flip_op(op_code):
    if op_code == OperationCode.NO_OP:
        flipped = OperationCode.JUMP
    elif op_code == OperationCode.JUMP:
        flipped = OperationCode.NO_OP
    else:
        flipped = op_code
    return flipped


def repair(computer):
    i = 0
    while computer.instruction_pointer < len(computer.code) and i < len(computer.code):
        computer.reset()
        computer.code[i].operation = flip_op(computer.code[i].operation)
        computer.execute_until_repeated()
        i += 1


class Computer:
    def __init__(self, code):
        self.original_code = copy.deepcopy(code)
        self.accumulator = None
        self.instruction_pointer = None
        self.code = None
        self.executed = None
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.instruction_pointer = 0
        self.code = copy.deepcopy(self.original_code)
        self.executed = []

    def get_this_operation(self):
        return self.code[self.instruction_pointer].operation

    def get_argument(self):
        return self.code[self.instruction_pointer].offset

    def execute_one(self):
        op = self.get_this_operation()
        if op == OperationCode.NO_OP:
            self.instruction_pointer += 1
        elif op == OperationCode.ACCUMULATE:
            self.accumulator += self.get_argument()
            self.instruction_pointer += 1
        elif op == OperationCode.JUMP:
            self.instruction_pointer += self.get_argument()

    def execute(self):
        while self.instruction_pointer < len(self.code):
            self.execute_one()

    def execute_until_repeated(self):
        while (self.instruction_pointer not in self.executed and self.instruction_pointer < len(self.code)):
            self.executed.append(self.instruction_pointer)
            self.execute_one()


class Instruction:
    def __init__(self, op, sign, offset):
        self.operation = self.parse_operation(op)
        self.offset = self.parse_offset(sign, offset)

    def __eq__(self, other):
        return self.operation == other.operation and \
               self.offset == other.offset

    def __str__(self):
        return "<Instruction: {0} {1}>".format(self.operation, self.offset)

    def __repr__(self):
        return self.__str__()

    def parse_offset(self, sign, offset):
        if sign == "+":
            return int(offset)
        elif sign == "-":
            return -1 * int(offset)
        else:
            raise UnknownCode

    def parse_operation(self, op):
        if op == "nop":
            return OperationCode.NO_OP
        elif op == "acc":
            return OperationCode.ACCUMULATE
        elif op == "jmp":
            return OperationCode.JUMP
        else:
            raise UnknownCode


def load_code(path):
    parser = re.compile("^(nop|acc|jmp) ([+-0])([0-9]+)$")
    raw_code = load_patterns(parser, path)
    code = [Instruction(inst[0], inst[1], inst[2]) for inst in raw_code]
    computer = Computer(code)
    return computer


def part_1(path):
    return load_one(path)


def part_2(path):
    return load_one(path)


if __name__ == "__main__":
    def main():
        computer = load_code("input/d08.txt")
        computer.execute_until_repeated()
        print("Accumulator {0}".format(computer.accumulator))

        computer.reset()
        repair(computer)
        print("Accumulator {0}".format(computer.accumulator))


    main()
