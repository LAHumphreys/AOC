from enum import Enum
from dataclasses import dataclass
from typing import Optional
from itertools import chain, tee
from copy import copy, deepcopy


def load_array(file_name: str) -> list[str]:
    with open(file_name) as input_file:
        return [ln.replace("\n", "") for ln in input_file.readlines()]


def tilt_up(array: list[str]) -> list[str]:
    next_idx = [0]*len(array[0])
    new_array = [["" for _ in range(len(array[0]))] for _ in range(len(array))]
    for row_n, row in enumerate(array):
        for col_n, col in enumerate(row):
            if col == ".":
                new_array[row_n][col_n] = "."
            elif col == "#":
                next_idx[col_n] = row_n + 1
                new_array[row_n][col_n] = "#"
            elif col == "O":
                if next_idx[col_n] < row_n:
                    new_array[next_idx[col_n]][col_n] = "O"
                    new_array[row_n][col_n] = "."
                    next_idx[col_n] += 1
                else:
                    new_array[row_n][col_n] = "O"
                    next_idx[col_n] = row_n + 1
            else:
                raise ValueError

    return ["".join(row) for row in new_array]


def debug_print(name: str, array: list[str]):
    print(f"{name}: ")
    for row in array:
        print("    "+row)


def rotate_clockwise(array: list[str]) -> list[str]:
    new_array = [""]*len(array)
    # top row is now right hand column
    for _, row in enumerate(array):
        for col_n, col in enumerate(row):
            new_array[col_n] = col + new_array[col_n]
    return new_array


def rotate_anticlockwise(array: list[str]) -> list[str]:
    new_array = [""]*len(array)
    # top row is now left column
    for _, row in enumerate(array):
        for col_n, col in enumerate(row):
            new_array[-1*(col_n+1)] += col
    return new_array


def tilt_left(array: list[str]) -> list[str]:
    new_array = rotate_clockwise(array)

    new_array = tilt_up(new_array)

    return rotate_anticlockwise(new_array)

def do_cycles(array: list[str], turns: int) -> list[str]:
    turn_tracker: dict[str, list[int]] = {}
    turn = 0
    while turn < turns:
        array = do_cycle(array)
        turn += 1
        key = "".join(array)
        if key in turn_tracker:
            turn_tracker[key] += [turn]
        else:
            turn_tracker[key] = [turn]
        if check_loop_to(turn_tracker[key], turns):
            return array
    return array


def check_loop_to(stops: list[int], target: int) -> bool:
    if len(stops) > 3:
        diff_1 = stops[-1] - stops[-2]
        diff_2 = stops[-2] - stops[-3]
        diff_3 = stops[-3] - stops[-4]
        if diff_1 != diff_2 or diff_1 != diff_3:
            return False
        remainder = target - stops[-1]
        if remainder % diff_1 == 0:
            return True
        else:
            return False
    return False

def do_cycle(array: list[str]) -> list[str]:
    for _ in range(4):
        array = tilt_up(array)
        array = rotate_clockwise(array)
    return array


def count_top_weight(array: list[str]) -> int:
    score = 0
    for row_n, row in enumerate(array):
        multiplier = len(array) - row_n
        score += sum(multiplier for c in row if c == "O")
    return score


def part_one(array: list[str]) -> int:
    tilted = tilt_up(array)
    return count_top_weight(tilted)


def part_two(array: list[str]) -> int:
    cycled_array = do_cycles(array, 1000000000)
    return count_top_weight(cycled_array)


def main():
    array = load_array("input/d14.txt")
    print(part_one(array))
    print(part_two(array))
    pass


if __name__ == "__main__":
    main()
