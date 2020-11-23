import copy
from tools.fileLoader import LoadIntList

def Add(prog, progPtr):
    inputIndxs = [prog[progPtr+1], prog[progPtr+2]]
    outIndx = prog[progPtr+3]
    prog[outIndx] = prog[inputIndxs[0]] + prog[inputIndxs[1]]

def Mul(prog, progPtr):
    inputIndxs = [prog[progPtr+1], prog[progPtr+2]]
    outIndx = prog[progPtr+3]
    prog[outIndx] = prog[inputIndxs[0]] * prog[inputIndxs[1]]

def Fixup1202(prog):
    prog[1] = 12
    prog[2] = 2

def Compute(input):
    prog = input
    exec = 0
    ins = prog[exec]
    while (ins != 99):
        if ins == 1:
            Add(prog, exec)
        elif ins == 2:
            Mul(prog, exec)

        exec += 4
        ins = prog[exec]

    return prog

def EncodeAnswer(noun, verb):
    return (100 * noun + verb)

class GravAssistCalc:
    def __init__(self):
        self.baseProg = prog = LoadIntList("input/d02.txt")

    def Compute(self, noun, verb):
        prog = copy.copy(self.baseProg)
        prog[1] = noun
        prog[2] = verb

        Compute(prog)

        return prog[0]

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


