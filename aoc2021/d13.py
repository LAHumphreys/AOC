from typing import Tuple, Dict, List
from tools.file_loader import load_lists


class Unhandled(Exception):
    pass


Point = Tuple[int, int]


def load_grid(path: str) -> Dict[Point, int]:
    return {tuple((int(x), int(y))): 1 for x, y in load_lists(path)}


def load_folds(path: str) -> List[Point]:
    folds = []
    with open (path, encoding="ascii") as file:
        for line in file.readlines():
            axis = line[11]
            if axis == "x":
                folds.append(tuple((int(line[13:]), None)))
            elif axis == "y":
                folds.append(tuple((None, int(line[13:]))))
            else:
                raise Unhandled
    return folds



def fold_fixed(point: Point, line: Point) -> Point:
    p_x, p_y = point
    x, y = line

    if x and y:
        raise Unhandled

    if y and (p_y > y):
        p_y = y - (p_y - y)

    if x and (p_x > x):
        p_x = x - (p_x - x)

    if p_x < 0 or p_y < 0:
        raise Unhandled

    return p_x, p_y


def fold_fixed_y(point: Point, y: int) -> Point:
    return fold_fixed(point, (None, y))


def fold_fixed_x(point: Tuple[int, int], x: int) -> Tuple[int, int]:
    return fold_fixed(point, (x, None))


def fold_grid(grid: Dict[Point, int], fold: Point) -> Dict[Point, int]:
    new_grid = {}
    for point in grid:
        new_point = fold_fixed(point, fold)
        if new_point not in new_grid:
            new_grid[new_point] = 1
        else:
            new_grid[new_point] += 1


    return new_grid


def part_one(grid: Dict[Point, int], folds: List[Point]) -> int:
    for fold in folds:
        grid = fold_grid(grid, fold)
    return len (grid)


def part_two(grid: Dict[Point, int], folds: List[Point]) -> int:
    for fold in folds:
        grid = fold_grid(grid, fold)

    max_x = 0
    max_y = 0
    for x, y in grid:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    output = ""
    for y in range(max_y+1):
        output += "\n"
        for x in range(max_x+1):
            if (x, y) in grid:
                output += "#"
            else:
                output += "."
    print (output)


if __name__ == "__main__":
    def main():
        folds = load_folds("input/d13/folds.txt")
        grid = load_grid("input/d13/grid.txt")
        print( part_one(grid, folds[0:1]))
        part_two(grid, folds)

    main()
