import copy

from aoc2019.compute import compute
from tools.fileLoader import load_int_list

if __name__ == "__main__":
    code = load_int_list("inp/d05.txt")
    inp = [1]
    output = []
    compute(copy.copy(code), inp=inp, output=output)
    print("Air con:")
    for o in output:
        print(o)

    inp = [5]
    output = []
    compute(copy.copy(code), inp=inp, output=output)
    print("Radiators:")
    for o in output:
        print(o)
