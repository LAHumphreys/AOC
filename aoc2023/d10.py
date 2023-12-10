from enum import Enum
from dataclasses import dataclass
from typing import Optional


class EnterFrom(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


Edge = EnterFrom

class PipeEnclosureState(Enum):
    UNTESTED = "."
    MARKED = "+"
    EXPOSED = "*"
    VERTICAL = "|"
    HORIZONTAL = "-"
    JOINT_F = "F"
    JOINT_L = "L"
    JOINT_J = "J"
    JOINT_7 = "7"


@dataclass
class NextSegment:
    x: int
    y: int
    enter_from: EnterFrom


@dataclass
class PipeSegment:
    next_segment: dict[EnterFrom, NextSegment]
    code: str


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
    return PipeSegment(next_segment=maps, code=symbol)


def traverse_pipe(enter_from: NextSegment, segment: PipeSegment) -> NextSegment:
    if enter_from.enter_from not in segment.next_segment:
        raise ValueError
    delta = segment.next_segment[enter_from.enter_from]
    return NextSegment(x=enter_from.x + delta.x,
                       y=enter_from.y + delta.y,
                       enter_from=delta.enter_from)


def apply_pipe_to_edges(edge: Edge, segment: PipeSegment, entered_from: EnterFrom) -> Edge:
    if segment.code == "|" or segment.code == "-":
        # No rotation performed
        return edge
    elif segment.code == "L":
        if entered_from == EnterFrom.TOP:
            if edge == Edge.LEFT:
                return Edge.BOTTOM
            elif edge == Edge.RIGHT:
                return Edge.TOP
        elif entered_from == EnterFrom.RIGHT:
            if edge == Edge.TOP:
                return Edge.RIGHT
            elif edge == Edge.BOTTOM:
                return Edge.LEFT
    elif segment.code == "J":
        if entered_from == EnterFrom.TOP:
            if edge == Edge.LEFT:
                return Edge.TOP
            elif edge == Edge.RIGHT:
                return Edge.BOTTOM
        elif entered_from == EnterFrom.LEFT:
            if edge == Edge.TOP:
                return Edge.LEFT
            elif edge == Edge.BOTTOM:
                return Edge.RIGHT
    elif segment.code == "F":
        if entered_from == EnterFrom.BOTTOM:
            if edge == Edge.LEFT:
                return Edge.TOP
            elif edge == Edge.RIGHT:
                return Edge.BOTTOM
        elif entered_from == EnterFrom.RIGHT:
            if edge == Edge.TOP:
                return Edge.LEFT
            elif edge == Edge.BOTTOM:
                return Edge.RIGHT
    elif segment.code == "7":
        if entered_from == EnterFrom.BOTTOM:
            if edge == Edge.LEFT:
                return Edge.BOTTOM
            elif edge == Edge.RIGHT:
                return Edge.TOP
        elif entered_from == EnterFrom.LEFT:
            if edge == Edge.TOP:
                return Edge.RIGHT
            elif edge == Edge.BOTTOM:
                return Edge.LEFT
    raise ValueError


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


def part_two(grid: InitialGrid) -> int:
    enclosure = draw_loop(grid)
    #mark_edges(enclosure)
    mark_outer_edges(enclosure, grid)
    debug_print(enclosure)
    resolve_marked_exposures(enclosure)
    debug_print(enclosure)
    return count_enclosed_area(enclosure)


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


def find_mark(enclosure: list[list[PipeEnclosureState]]) -> Optional[tuple[int, int]]:
    for y, row in enumerate(enclosure):
        for x, state in enumerate(row):
            if state == PipeEnclosureState.MARKED:
                return x, y
    return None


def resolve_marked_exposures(enclosure: list[list[PipeEnclosureState]]):
    next_mark = find_mark(enclosure)
    while next_mark:
        x, y = next_mark
        expose_cell(enclosure, x, y)
        next_mark = find_mark(enclosure)


def debug_print(cells: list[list[PipeEnclosureState]]):
    for row in cells:
        print("".join([x.value for x in row]))


def expose_cell(enclosure: list[list[PipeEnclosureState]], x: int, y: int):
    enclosure[y][x] = PipeEnclosureState.EXPOSED
    max_x = len(enclosure[0]) - 1
    max_y = len(enclosure) - 1
    mark_x, mark_y = x, y
    vertical_states = [PipeEnclosureState.HORIZONTAL, PipeEnclosureState.MARKED, PipeEnclosureState.EXPOSED]
    horizontal_states = [PipeEnclosureState.VERTICAL, PipeEnclosureState.MARKED, PipeEnclosureState.EXPOSED]

    def check_if_requires_vertical_propagation(check_x: int, check_y: int):
        if check_y > 0 and enclosure[check_y - 1][check_x] not in vertical_states:
            return True
        if check_y < max_y and enclosure[check_y + 1][check_x] not in vertical_states:
            return True
        return False

    def check_if_requires_horizontal_propagation(check_x: int, check_y: int):
        if check_x > 0 and enclosure[check_y][check_x - 1] not in horizontal_states:
            return True
        if check_x < max_x and enclosure[check_y][check_x + 1] not in horizontal_states:
            return True
        return False

    closed_lower_gap_joints = [PipeEnclosureState.JOINT_F, PipeEnclosureState.JOINT_7]
    closed_upper_gap_joints = [PipeEnclosureState.JOINT_J, PipeEnclosureState.JOINT_L]
    closed_left_gap_joints = [PipeEnclosureState.JOINT_7, PipeEnclosureState.JOINT_J]
    closed_right_gap_joints = [PipeEnclosureState.JOINT_F, PipeEnclosureState.JOINT_L]

    def close_horizontal_gaps(check_x: int, check_y: int, lower: bool, upper: bool):
        if enclosure[check_y][check_x] == PipeEnclosureState.VERTICAL:
            lower = upper = False
        elif enclosure[check_y][check_x] in closed_lower_gap_joints:
            lower = False
        elif enclosure[check_y][check_x] in closed_upper_gap_joints:
            upper = False

        return lower, upper

    def close_vertical_gaps(check_x: int, check_y: int, left: bool, right: bool):
        if enclosure[check_y][check_x] == PipeEnclosureState.HORIZONTAL:
            left = right = False
        elif enclosure[check_y][check_x] in closed_left_gap_joints:
            left = False
        elif enclosure[check_y][check_x] in closed_right_gap_joints:
            right = False

        return left, right

    lower_gap = upper_gap = True
    while mark_x > 0 and (lower_gap or upper_gap):
        mark_x -= 1
        lower_gap, upper_gap = close_horizontal_gaps(mark_x, mark_y, lower_gap, upper_gap)
        if enclosure[y][mark_x] == PipeEnclosureState.UNTESTED:
            if check_if_requires_vertical_propagation(mark_x, y):
                enclosure[y][mark_x] = PipeEnclosureState.MARKED
            else:
                enclosure[y][mark_x] = PipeEnclosureState.EXPOSED

    mark_x, mark_y = x, y
    lower_gap = upper_gap = True
    while mark_x < max_x and (lower_gap or upper_gap):
        mark_x += 1
        lower_gap, upper_gap = close_horizontal_gaps(mark_x, mark_y, lower_gap, upper_gap)
        if enclosure[y][mark_x] == PipeEnclosureState.UNTESTED:
            if check_if_requires_vertical_propagation(mark_x, y):
                enclosure[y][mark_x] = PipeEnclosureState.MARKED
            else:
                enclosure[y][mark_x] = PipeEnclosureState.EXPOSED

    mark_x, mark_y = x, y
    left_gap = right_gap = True
    while mark_y > 0 and (left_gap or right_gap):
        mark_y -= 1
        left_gap, right_gap = close_vertical_gaps(x, mark_y, left_gap, right_gap)
        if enclosure[mark_y][x] == PipeEnclosureState.UNTESTED:
            if check_if_requires_horizontal_propagation(x, mark_y):
                enclosure[mark_y][x] = PipeEnclosureState.MARKED
            else:
                enclosure[mark_y][x] = PipeEnclosureState.EXPOSED

    mark_y, mark_y = x, y
    left_gap = right_gap = True
    while mark_y < max_y and (left_gap or right_gap):
        mark_y += 1
        left_gap, right_gap = close_vertical_gaps(x, mark_y, left_gap, right_gap)
        if enclosure[mark_y][x] == PipeEnclosureState.UNTESTED:
            if check_if_requires_horizontal_propagation(x, mark_y):
                enclosure[mark_y][x] = PipeEnclosureState.MARKED
            else:
                enclosure[mark_y][x] = PipeEnclosureState.EXPOSED


def load_enclosure(file_name: str) -> list[list[PipeEnclosureState]]:
    with open(file_name) as input_file:
        grid = []
        for line in (line.replace("\n", "") for line in input_file.readlines()):
            grid += [[PipeEnclosureState(c) for c in line]]
        return grid


def draw_loop(grid: InitialGrid) -> list[list[PipeEnclosureState]]:
    enclosure: list[list[PipeEnclosureState]] = []
    for row in grid.pipes:
        enclosure += [[PipeEnclosureState.UNTESTED for _ in row]]

    start_pos = grid.pipes[grid.start_y][grid.start_x]
    route = [x for x in start_pos.next_segment.keys()][0]
    start_segment = NextSegment(x=grid.start_x, y=grid.start_y, enter_from=route)
    current_location = traverse_pipe(start_segment, start_pos)
    enclosure[grid.start_y][grid.start_x] = PipeEnclosureState(grid.pipes[grid.start_y][grid.start_x].code)
    enclosure[current_location.y][current_location.x] = \
        PipeEnclosureState(grid.pipes[current_location.y][current_location.x].code)
    while current_location.x != grid.start_x or current_location.y != grid.start_y:
        current_segment = grid.pipes[current_location.y][current_location.x]
        current_location = traverse_pipe(current_location, current_segment)
        enclosure[current_location.y][current_location.x] = \
            PipeEnclosureState(grid.pipes[current_location.y][current_location.x].code)
    return enclosure


def mark_edges(enclosure: list[list[PipeEnclosureState]]):
    max_x = len(enclosure[0]) - 1
    exposed_row = [PipeEnclosureState.MARKED] * (max_x +3)
    for row in enclosure:
        row.insert(0, PipeEnclosureState.MARKED)
        row.append(PipeEnclosureState.MARKED)
    enclosure.insert(0, exposed_row)
    enclosure.append(exposed_row)

def find_left_edge(enclosure: list[list[PipeEnclosureState]]) -> tuple[int, int]:
    for y in range(len(enclosure)):
        for x in range(len(enclosure[0])):
            if enclosure[y][x] == PipeEnclosureState.VERTICAL:
                return x, y
            elif enclosure[y][x] != PipeEnclosureState.UNTESTED:
                break
    raise ValueError


def mark_outer_edges(enclosure: list[list[PipeEnclosureState]], grid: InitialGrid):
    start_x, start_y = find_left_edge(enclosure)
    max_y = len(enclosure) - 1
    max_x = len(enclosure[0]) - 1

    def mark_current_edge():
        if edge == Edge.TOP and current_location.y > 0 and \
                enclosure[current_location.y-1][current_location.x] == PipeEnclosureState.UNTESTED:
            enclosure[current_location.y - 1][current_location.x] = PipeEnclosureState.MARKED
        if edge == Edge.BOTTOM and current_location.y < max_y and \
                enclosure[current_location.y + 1][current_location.x] == PipeEnclosureState.UNTESTED:
            enclosure[current_location.y + 1][current_location.x] = PipeEnclosureState.MARKED
        if edge == Edge.LEFT and current_location.x > 0 and \
                enclosure[current_location.y][current_location.x-1] == PipeEnclosureState.UNTESTED:
            enclosure[current_location.y][current_location.x-1] = PipeEnclosureState.MARKED
        if edge == Edge.RIGHT and current_location.x < max_x and \
                enclosure[current_location.y][current_location.x + 1] == PipeEnclosureState.UNTESTED:
            enclosure[current_location.y][current_location.x + 1] = PipeEnclosureState.MARKED

    edge = Edge.LEFT
    start_pipe = grid.pipes[start_y][start_x]
    start_segment = NextSegment(x=start_x, y=start_y, enter_from=EnterFrom.BOTTOM)
    current_location = traverse_pipe(start_segment, start_pipe)
    edge = apply_pipe_to_edges(edge, start_pipe, start_segment.enter_from)
    mark_current_edge()
    while current_location.x != start_x or current_location.y != start_y:
        current_pipe = grid.pipes[current_location.y][current_location.x]
        edge = apply_pipe_to_edges(edge, current_pipe, current_location.enter_from)

        mark_current_edge()
        current_location = traverse_pipe(current_location, current_pipe)
        mark_current_edge()



def count_enclosed_area(enclosure: list[list[PipeEnclosureState]]) -> int:
    total = 0
    for row in range(len(enclosure)):
        for col in range(len(enclosure[0])):
            if enclosure[row][col] == PipeEnclosureState.UNTESTED:
                total += 1
    return total


def main():
    grid = load_grid_with_start("input/d10.txt")
    print(part_one(grid))
    print(part_two(grid))
    pass


if __name__ == "__main__":
    main()
