from tools.listOps import FindSumPair
from tools.fileLoader import LoadInts

def FindProduct(numbers: list):
    [low, high]  = FindSumPair(numbers, 2020)
    return low * high

if __name__ == "__main__":
    numbers = LoadInts("input/d01.txt")
    print(FindProduct(numberk))