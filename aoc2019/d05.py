import copy

from aoc2019.compute import compute
from tools.file_loader import load_int_list

if __name__ == "__main__":
    def main():
        code = load_int_list("input/d05.txt")
        inp = [1]
        output = []
        compute(copy.copy(code), inp=inp, output=output)
        print("Air con:")
        for out in output:
            print(out)

        inp = [5]
        output = []
        compute(copy.copy(code), inp=inp, output=output)
        print("Radiators:")
        for out in output:
            print(out)


    main()
