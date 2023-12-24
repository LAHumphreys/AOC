from enum import Enum
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Garden:
    plots: list[str]
    len_x: int
    len_y: int


def load_garden(file_name) -> Garden:
    with open(file_name) as input_file:
        plot = [line.replace("\n", "").replace("S", "O") for line in input_file.readlines()]
        return Garden(
            plots=plot, len_x=len(plot[0]), len_y=len(plot))


def expand_garden(garden: Garden) -> Garden:
    plots = [row.replace("O", ".")*5 for row in garden.plots]
    plots = plots * 5
    # OK - but we need to replace the S
    for x, row in enumerate(garden.plots):
        for y, space in enumerate(row):
            if space == "O":
                without_S = row.replace("O", ".")
                plots[y+2*garden.len_y] = without_S*2 + row + without_S*2

    return Garden(plots=plots, len_x=len(plots[0]), len_y=len(plots))


def mark_possible_steps(plot: list[list[str]], x: int, y: int, max_x: int, max_y: int):
    if x > 0 and plot[y][x-1] != "#":
        plot[y][x-1] = "O"
    if x < max_x and plot[y][x+1] != "#":
        plot[y][x+1] = "O"
    if y > 0 and plot[y-1][x] != "#":
        plot[y-1][x] = "O"
    if y < max_y and plot[y+1][x] != "#":
        plot[y+1][x] = "O"


def apply_step(garden: Garden) -> Garden:
    new_plot = [[x for x in row.replace("O", ".")] for row in garden.plots]
    for y, row in enumerate(garden.plots):
        for x, space in enumerate(row):
            if space == "O":
                mark_possible_steps(new_plot, x, y, garden.len_x-1, garden.len_y-1)
    return Garden(
        len_x=garden.len_x,
        len_y=garden.len_y,
        plots=["".join(row) for row in new_plot]
    )


def debug_print(garden: Garden):
    for row in garden.plots:
        print(row)
    print("")


def apply_steps(garden: Garden, count: int) -> Garden:
    while count > 0:
        garden = apply_step(garden)
        debug_print(garden)
        count -= 1
    return garden


def count_options(garden: Garden) -> int:
    return sum(sum(x == "O" for x in row) for row in garden.plots)


def part_one(garden: Garden) -> int:
    updated = apply_steps(garden, 64)
    return count_options(updated)


def main():
    garden = load_garden("input/d21.txt")
    print(part_one(garden))
    pass


if __name__ == "__main__":
    main()
