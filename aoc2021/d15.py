from typing import Tuple, List
from copy import copy


def enlarge_map(num_tiles: int, cave_map: List[List[int]]) -> List[List[int]]:
    dimensions = (len(cave_map[0]), len(cave_map))
    result = [[-1] * dimensions[0] * num_tiles for _ in range(dimensions[1]*num_tiles)]
    for y in range(num_tiles):
        for x in range(num_tiles):
            tile_no = x + y
            for source_x in range(dimensions[0]):
                for source_y in range(dimensions[1]):
                    cost = cave_map[source_y][source_x] + tile_no
                    if cost > 9:
                        cost -= 9
                    result[source_y + y*dimensions[1]][source_x + x*dimensions[0]] = cost
    return result


def load_map(path: str) -> List[List[int]]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    result = []
    for line in lines:
        result.append([int(x) for x in line])
    return result


def get_points_to_check(point: Tuple[int, int], dimensions: Tuple[int, int]):
    x, y = point
    if x > 0:
        yield x - 1, y
    if x < dimensions[0]-1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < dimensions[1]-1:
        yield x, y + 1


def calc_cost_map(cave_map: List[List[int]],
                  destination: Tuple[int, int] = None) -> List[List[int]]:
    dimensions = (len(cave_map[0]), len(cave_map))
    if not destination:
        destination = (dimensions[0]-1, dimensions[1] - 1)
    cost_map = [[-1]*dimensions[0] for _ in range(dimensions[1])]

    cost_map[destination[1]][destination[0]] = 0
    to_check = {copy(destination)}
    while to_check:
        point = to_check.pop()
        cost = cost_map[point[1]][point[0]] + cave_map[point[1]][point[0]]
        for x, y in get_points_to_check(point, dimensions):
            current_best_cost = cost_map[y][x]
            if current_best_cost == -1 or current_best_cost > cost:
                cost_map[y][x] = cost
                to_check.add((x, y))

    return cost_map


if __name__ == "__main__":
    def main():
        cave_map = load_map("input/d15.txt")
        cost_map = calc_cost_map(cave_map)
        print(cost_map[0][0])
        enlarged_map = enlarge_map(5, cave_map)
        enlarged_costs = calc_cost_map(enlarged_map)
        print(enlarged_costs[0][0])
    main()
