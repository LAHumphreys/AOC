import copy
from os.path import dirname, abspath, join

from aoc2019.compute import compute, encode, Instruction, encode_compute
from tools.file_loader import load_int_list


def make_path(path):
    dir_path = dirname(abspath(__file__))
    return join(dir_path, path)


def fixup_1202(program):
    program[1] = 12
    program[2] = 2


def encode_answer(noun, verb):
    return 100 * noun + verb


class GravAssistCalc:
    def __init__(self):
        self.base_program = encode(load_int_list(make_path("input/d02.txt")))

    def get_code(self):
        return copy.copy(self.base_program)

    def compute(self, noun, verb):
        program = self.get_code()
        program[1] = Instruction(noun)
        program[2] = Instruction(verb)

        return encode_compute(program)[0].get_value()


def find_verb_noun(target):
    calc = GravAssistCalc()
    for noun in range(0, 100):
        for verb in range(0, 100):
            if calc.compute(noun, verb) == target:
                return [verb, noun]
    return [-1, -1]


def find_and_encode(target):
    [verb, noun] = find_verb_noun(target)
    return encode_answer(noun, verb)


if __name__ == "__main__":
    def main():
        program = load_int_list("input/d02.txt")
        fixup_1202(program)
        compute(program)
        print(program[0])
        print(find_and_encode(19690720))

    main()
