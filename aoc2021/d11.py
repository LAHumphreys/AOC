import copy
from typing import List

neighbours = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
]


def flash_octopus(tangle: List[List[int]], column: int, row: int) -> List[List[int]]:
    tangle[row][column] = 0
    for neighbour_x, neighbour_y in neighbours:
        neighbour_x += column
        neighbour_y += row
        if 0 <= neighbour_y < len(tangle) and 0 <= neighbour_x < len(tangle[neighbour_y]):
            if tangle[neighbour_y][neighbour_x] > 0:
                tangle[neighbour_y][neighbour_x] += 1

    return tangle


def do_steps(tangle: List[List[int]], num_steps: int) -> int:
    flashed = 0
    for _ in range(num_steps):
        flashed += do_step(tangle)

    return flashed


def do_step(tangle: List[List[int]]) -> int:
    for row, tangle_row in enumerate(tangle):
        for column, octopus in enumerate(tangle_row):
            tangle[row][column] += 1

    flashed = 0
    more_flashes = True
    while more_flashes:
        more_flashes = False
        for row, tangle_row in enumerate(tangle):
            for column, octopus in enumerate(tangle_row):
                if octopus > 9:
                    flash_octopus(tangle, column, row)
                    more_flashes = True
                    flashed += 1

    return flashed


def load_tangle(path: str) -> List[List[int]]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    result = []
    for line in lines:
        result.append([int(octopus) for octopus in line])
    return result


def find_simultaneous_flash(tangle: List[List[int]]) -> int:
    num_octopuses = len(tangle) * len(tangle[0])
    steps = 0
    flashed = 0
    while flashed != num_octopuses:
        flashed = do_step(tangle)
        steps += 1
    return steps


if __name__ == "__main__":
    def main():
        tangle = load_tangle("input/d11.txt")
        print(do_steps(copy.deepcopy(tangle), 100))
        print(find_simultaneous_flash(copy.deepcopy(tangle)))
    main()
