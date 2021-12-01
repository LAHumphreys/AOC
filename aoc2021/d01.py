from tools.file_loader import load_ints
from typing import List


def count_increases(numbers: List[int]):
    return count_windows(numbers, 1)


def count_trios(numbers: List[int]):
    return count_windows(numbers, 3)


def count_windows(numbers: List[int], win_size: int):
    count: int = 0
    for i in range(win_size, len(numbers)):
        if numbers[i] > numbers[i-win_size]:
            count += 1

    return count


if __name__ == "__main__":
    def main():
        numbers = load_ints("input/d01.txt")
        print(count_increases(numbers))
        print(count_trios(numbers))
    main()
