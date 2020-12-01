import copy

from tools.fileLoader import LoadIntList
from aoc2019.compute import Compute, Encode, Instruction, EncodedCompute

if __name__ == "__main__":
    code = LoadIntList("input/d05.txt")
    input = [1]
    output = []
    Compute(copy.copy(code), input=input, output=output)
    print ("Air con:")
    for o in output:
        print(o)

    input = [5]
    output = []
    Compute(copy.copy(code), input=input, output=output)
    print ("Radiators:")
    for o in output:
        print(o)
