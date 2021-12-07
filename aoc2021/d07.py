from typing import List
from tools.file_loader import load_int_list


def count_fuel(target: int, positions: List[int]) -> int:
    return sum((abs(target - pos) for pos in positions))


def count_expo_steps(start_pos: int, end_pos: int) -> int:
    # moving N steps = 1 + 2 + 3 + ... + (N-2) + (N-1) + N
    # ==> Pair from start and end, and don't forget the middle term for odd N:
    #     (N+1) * (N//2) + [(1+N//2) if odd]
    steps = abs(end_pos - start_pos)
    return (steps+1) * (steps//2) + (steps % 2) * ((steps+1) // 2)


def count_expo_fuel(target: int, positions: List[int]) -> int:
    return sum((count_expo_steps(target, pos) for pos in positions))


def find_mid(positions: List[int]) -> int:
    positions.sort()
    return positions[len(positions) // 2]


def part_one(positions: List[int]) -> int:
    return count_fuel(find_mid(positions), positions)


def part_two(positions: List[int]) -> int:
    guess = find_mid(positions)
    costs = [
        count_expo_fuel(guess - 1, positions),
        count_expo_fuel(guess, positions),
        count_expo_fuel(guess + 1, positions),
    ]
    keep_looking = True
    while keep_looking:
        if costs[1] > costs[0]:
            guess -= 1
            costs = [count_expo_fuel(guess-1, positions)] + costs[0:2]
        elif costs[1] > costs[2]:
            guess += 1
            costs = costs[1:] + [count_expo_fuel(guess+1, positions)]
        else:
            keep_looking = False

    return costs[1]


if __name__ == "__main__":
    def main():
        positions = load_int_list("input/d07.txt")
        print(part_one(positions))
        print(part_two(positions))
    main()
