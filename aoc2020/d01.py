from tools.file_loader import load_ints
from tools.list_ops import find_sum_pair, find_sum_trio


def find_product(numbers: list):
    [low, high] = find_sum_pair(numbers, 2020)
    return low * high


def find_trio_product(numbers: list):
    [low, mid, high] = find_sum_trio(numbers, 2020)
    return low * mid * high


if __name__ == "__main__":
    def main():
        numbers = load_ints("input/d01.txt")
        print(find_product(numbers))
        print(find_trio_product(numbers))

    main()
