from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class LocalMinimum:
    x: int
    y: int
    value: int


def get_adjacent(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def find_minimums(dataset: List[List[int]]) -> List[LocalMinimum]:
    result = []
    y_boundary = len(dataset)
    x_boundary = len(dataset[0])
    for x in range(x_boundary):
        for y in range(y_boundary):
            value = dataset[y][x]
            indexes = get_adjacent(x, y)
            minimum = True
            for i_x, i_y in indexes:
                if 0 <= i_x < x_boundary and 0 <= i_y < y_boundary and dataset[i_y][i_x] <= value:
                    minimum = False
            if minimum:
                result.append(LocalMinimum(x, y, value))
    return result


def get_basin_size(dataset: List[List[int]], start_x, start_y) -> int:
    def make_key(key_x, key_y) -> str:
        return f"{key_x}:{key_y}"

    boundaries = (len(dataset[0]), len(dataset))
    stack = [(start_x, start_y)]
    checked = set()
    counted = {make_key(start_x, start_y)}

    while stack:
        x, y = stack.pop()
        to_check = get_adjacent(x, y)
        value = dataset[y][x]
        for check_x, check_y in to_check:
            if 0 <= check_x < boundaries[0] and \
                    0 <= check_y < boundaries[1] and \
                    value < dataset[check_y][check_x] < 9:
                new_key = make_key(check_x, check_y)
                if new_key not in checked:
                    checked.add(new_key)
                    stack.append((check_x, check_y))
                    counted.add(new_key)

    return len(counted)


def convert_data_row(row: str) -> List[int]:
    result = []
    for column in row:
        if column != "\n":
            result.append(int(column))
    return result


def load_data_rows(path: str) -> List[List[int]]:
    with open(path, encoding="ascii") as file:
        data = [convert_data_row(line) for line in file.readlines()]
    return data


def part_one(dataset: List[List[int]]) -> int:
    return sum(minimum.value + 1 for minimum in find_minimums(dataset))


def part_two(dataset: List[List[int]]) -> int:
    basins = [get_basin_size(dataset, minimum.x, minimum.y) for minimum in find_minimums(dataset)]
    basins.sort()
    return basins[-1] * basins[-2] * basins[-3]


if __name__ == "__main__":
    def main():
        data = load_data_rows("input/d09.txt")
        print(part_one(data))
        print(part_two(data))


    main()
