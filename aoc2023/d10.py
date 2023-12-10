from enum import Enum
from dataclasses import dataclass
from typing import Optional


class EnterFrom(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


class PipeEnclosureState(Enum):
    EMPTY = "."
    VERTICAL = "|"
    HORIZONTAL = "-"
    JOINT = "?"


@dataclass
class NextSegment:
    x: int
    y: int
    enter_from: EnterFrom


@dataclass
class PipeSegment:
    next_segment: dict[EnterFrom, NextSegment]


def make_segment(symbol: str) -> Optional[PipeSegment]:
    maps: dict[EnterFrom, NextSegment] = {}
    if symbol == "|":
        maps[EnterFrom.TOP] = NextSegment(x=0, y=1, enter_from=EnterFrom.TOP)
        maps[EnterFrom.BOTTOM] = NextSegment(x=0, y=-1, enter_from=EnterFrom.BOTTOM)
    elif symbol == "-":
        maps[EnterFrom.LEFT] = NextSegment(x=1, y=0, enter_from=EnterFrom.LEFT)
        maps[EnterFrom.RIGHT] = NextSegment(x=-1, y=0, enter_from=EnterFrom.RIGHT)
    elif symbol == "L":
        maps[EnterFrom.TOP] = NextSegment(x=1, y=0, enter_from=EnterFrom.LEFT)
        maps[EnterFrom.RIGHT] = NextSegment(x=0, y=-1, enter_from=EnterFrom.BOTTOM)
    elif symbol == "J":
        maps[EnterFrom.TOP] = NextSegment(x=-1, y=0, enter_from=EnterFrom.RIGHT)
        maps[EnterFrom.LEFT] = NextSegment(x=0, y=-1, enter_from=EnterFrom.BOTTOM)
    elif symbol == "7":
        maps[EnterFrom.BOTTOM] = NextSegment(x=-1, y=0, enter_from=EnterFrom.RIGHT)
        maps[EnterFrom.LEFT] = NextSegment(x=0, y=1, enter_from=EnterFrom.TOP)
    elif symbol == "F":
        maps[EnterFrom.RIGHT] = NextSegment(x=0, y=1, enter_from=EnterFrom.TOP)
        maps[EnterFrom.BOTTOM] = NextSegment(x=1, y=0, enter_from=EnterFrom.LEFT)
    else:
        return None
    return PipeSegment(next_segment=maps)


def traverse_pipe(enter_from: NextSegment, segment: PipeSegment) -> NextSegment:
    if enter_from.enter_from not in segment.next_segment:
        raise ValueError
    delta = segment.next_segment[enter_from.enter_from]
    return NextSegment(x=enter_from.x + delta.x,
                       y=enter_from.y + delta.y,
                       enter_from=delta.enter_from)


def determine_start(grid: list[list[PipeSegment]], start_x, start_y) -> PipeSegment:
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    has_right_exit = start_x < max_x and\
        grid[start_y][start_x + 1] and \
        EnterFrom.LEFT in grid[start_y][start_x + 1].next_segment
    has_left_exit = start_x > 0 and \
        grid[start_y][start_x + -1] and \
        EnterFrom.RIGHT in grid[start_y][start_x + -1].next_segment
    has_top_exit = start_y > 0 and \
        grid[start_y - 1][start_x] and \
        EnterFrom.BOTTOM in grid[start_y - 1][start_x].next_segment
    has_bottom_exit = start_y < max_y and \
        grid[start_y + 1][start_x] and \
        EnterFrom.TOP in grid[start_y + 1][start_x].next_segment

    if has_bottom_exit and has_right_exit:
        return make_segment("F")

    if has_left_exit and has_right_exit:
        return make_segment("-")

    if has_left_exit and has_bottom_exit:
        return make_segment("7")

    if has_top_exit and has_bottom_exit:
        return make_segment("|")

    if has_top_exit and has_right_exit:
        return make_segment("L")

    if has_left_exit and has_top_exit:
        return make_segment("J")

    raise ValueError


def find_start(lines: list[str]) -> Optional[tuple[int, int]]:
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                return x, y
    return None


@dataclass
class InitialGrid:
    pipes: list[list[PipeSegment]]
    start_x: Optional[int]
    start_y: Optional[int]


def load_grid_with_start(file_name: str) -> InitialGrid:
    with open(file_name) as input_file:
        grid = []
        lines = [line.replace("\n", "") for line in input_file.readlines()]
        for line in lines:
            grid += [[make_segment(x) for x in line]]

        start = find_start(lines)
        if start:
            start_x, start_y = start
            grid[start_y][start_x] = determine_start(grid, start_x, start_y)
        else:
            start_x, start_y = None, None

    return InitialGrid(pipes=grid, start_x=start_x, start_y=start_y)


def load_grid(file_name: str) -> list[list[PipeSegment]]:
    return load_grid_with_start(file_name).pipes


def part_one(grid: InitialGrid) -> int:
    start_pos = grid.pipes[grid.start_y][grid.start_x]
    starts: list[NextSegment] = []
    for route in start_pos.next_segment.keys():
        start_segment = NextSegment(x=grid.start_x, y=grid.start_y, enter_from=route)
        starts += [traverse_pipe(start_segment, start_pos)]
    first, second = starts
    steps = 1
    while first.x != second.x or first.y != second.y:
        first = traverse_pipe(first, grid.pipes[first.y][first.x])
        second = traverse_pipe(second, grid.pipes[second.y][second.x])
        steps += 1
    return steps



def is_enclosed(enclosure: list[list[PipeEnclosureState]], start_x: int, start_y: int):
    if enclosure[start_y][start_x] != PipeEnclosureState.EMPTY:
        return False
    max_x = len(enclosure[0]) - 1
    max_y = len(enclosure) - 1

    enclosed = False
    x, y = start_x, start_y
    while not enclosed and x > 0:
        x -= 1
        enclosed = enclosure[start_y][x] == PipeEnclosureState.VERTICAL
    if not enclosed:
        return False

    enclosed = False
    x, y = start_x, start_y
    while not enclosed and x < max_x:
        x += 1
        enclosed = enclosure[start_y][x] == PipeEnclosureState.VERTICAL
    if not enclosed:
        return False

    x, y = start_x, start_y
    enclosed = False
    while not enclosed and y < max_y:
        y += 1
        enclosed = enclosure[y][start_x] == PipeEnclosureState.HORIZONTAL
    if not enclosed:
        return False

    x, y = start_x, start_y
    enclosed = False
    while not enclosed and y > 0:
        y -= 1
        enclosed = enclosure[y][start_x] == PipeEnclosureState.HORIZONTAL
    if not enclosed:
        return False

    return True


def load_enclosure(file_name: str) -> list[list[PipeEnclosureState]]:
    with open(file_name) as input_file:
        grid = []
        for line in (line.replace("\n", "") for line in input_file.readlines()):
            row = []
            for c in line:
                if c == ".":
                    row += [PipeEnclosureState.EMPTY]
                elif c == "|":
                    row += [PipeEnclosureState.VERTICAL]
                elif c == "-":
                    row += [PipeEnclosureState.HORIZONTAL]
                else:
                    row += [PipeEnclosureState.JOINT]
            grid += [row]
        return grid


def count_enclosed_area(enclosure: list[list[PipeEnclosureState]]) -> int:
    total = 0
    for row in range(len(enclosure)):
        for col in range(len(enclosure[0])):
            if is_enclosed(enclosure, col, row):
                total += 1
    return total


def main():
    grid = load_grid_with_start("input/d10.txt")
    print(part_one(grid))
    pass


if __name__ == "__main__":
    main()
