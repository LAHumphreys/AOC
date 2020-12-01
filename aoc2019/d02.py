import copy
from tools.fileLoader import LoadIntList
from aoc2019.compute import Compute, Encode, Instruction, EncodedCompute

def Fixup1202(prog):
    prog[1] = 12
    prog[2] = 2

def EncodeAnswer(noun, verb):
    return (100 * noun + verb)

class GravAssistCalc:
    def __init__(self):
        self.baseProg = Encode(LoadIntList("input/d02.txt"))

    def Compute(self, noun, verb):
        prog = copy.copy(self.baseProg)
        prog[1] = Instruction(noun)
        prog[2] = Instruction(verb)

        return EncodedCompute(prog)[0].GetValue()

def FindVerbNoun(target):
    calc = GravAssistCalc()
    for noun in range(0, 100):
        for verb in range(0, 100):
            if calc.Compute(noun, verb) == target:
                return [verb, noun]
    return [-1, -1]

def FindAndEncode(target):
    [verb, noun] = FindVerbNoun(target)
    return EncodeAnswer(noun, verb)


if __name__ == "__main__":
    prog = LoadIntList("input/d02.txt")
    Fixup1202(prog)
    Compute(prog)
    print (prog[0])
    print (FindAndEncode(19690720))


