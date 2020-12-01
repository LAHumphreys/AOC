from tools.listOps import FindSumPair, FindSumTrio
from tools.fileLoader import LoadInts

def FindProduct(numbers: list):
    [low, high]  = FindSumPair(numbers, 2020)
    return low * high

def FindTrioProduct(numbers: list):
    [low, mid, high]  = FindSumTrio(numbers, 2020)
    return low * mid * high

if __name__ == "__main__":
    numbers = LoadInts("input/d01.txt")
    print(FindProduct(numbers))
    print(FindTrioProduct(numbers))

