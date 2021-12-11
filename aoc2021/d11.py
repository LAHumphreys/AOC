import copy
from typing import List

neighbours = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
]


def flash_octopus(tentacle: List[List[int]], column: int, row: int) -> List[List[int]]:
    tentacle[row][column] = 0
    for neighbour_x, neighbour_y in neighbours:
        neighbour_x += column
        neighbour_y += row
        if 0 <= neighbour_y < len(tentacle) and 0 <= neighbour_x < len(tentacle[neighbour_y]):
            if tentacle[neighbour_y][neighbour_x] > 0:
                tentacle[neighbour_y][neighbour_x] += 1

    return tentacle


def do_steps(tentacle: List[List[int]], num_steps: int) -> int:
    flashed = 0
    for _ in range(num_steps):
        flashed += do_step(tentacle)

    return flashed


def do_step(tentacle: List[List[int]]) -> int:
    for row, tentacle_row in enumerate(tentacle):
        for column, octopus in enumerate(tentacle_row):
            tentacle[row][column] += 1

    flashed = 0
    more_flashes = True
    while more_flashes:
        more_flashes = False
        for row, tentacle_row in enumerate(tentacle):
            for column, octopus in enumerate(tentacle_row):
                if octopus > 9:
                    flash_octopus(tentacle, column, row)
                    more_flashes = True
                    flashed += 1

    return flashed


def load_tentacle(path: str) -> List[List[int]]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    result = []
    for line in lines:
        result.append([int(octopus) for octopus in line])
    return result


def find_simultaneous_flash(tentacle: List[List[int]]) -> int:
    num_octopuses = len(tentacle) * len(tentacle[0])
    steps = 0
    flashed = 0
    while flashed != num_octopuses:
        flashed = do_step(tentacle)
        steps += 1
    return steps


if __name__ == "__main__":
    def main():
        tentacle = load_tentacle("input/d11.txt")
        print(do_steps(copy.deepcopy(tentacle), 100))
        print(find_simultaneous_flash(copy.deepcopy(tentacle)))
    main()
