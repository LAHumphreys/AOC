from dataclasses import dataclass
from itertools import combinations
from copy import deepcopy


@dataclass
class UniverseLocation:
    x: int
    y: int


def load_galaxy(file_name: str) -> list[str]:
    with open(file_name, encoding='utf-8') as input_file:
        return [ln.replace("\n", "") for ln in input_file.readlines()]


def expand_universe(universe: list[str], expansion_size: int = 1) -> list[str]:
    expanded = []
    for row in universe:
        if "#" in row:
            expanded.append(deepcopy(row))
        else:
            expanded.append(deepcopy(row))
            for _ in range(expansion_size):
                expanded.append(deepcopy(row))
    universe = expanded
    expanded = [""] * len(universe)
    for x in range(len(universe[0])):
        empty = True
        for y, row in enumerate(universe):
            location = row[x]
            if location == "#":
                empty = False
            expanded[y] += location
        if empty:
            for y in range(len(universe)):
                for _ in range(expansion_size):
                    expanded[y] += "."

    return expanded


def galaxy_distance(galaxy1: UniverseLocation, galaxy2: UniverseLocation) -> int:
    return max(galaxy2.x, galaxy1.x) - min(galaxy2.x, galaxy1.x) + \
           max(galaxy2.y, galaxy1.y) - min(galaxy2.y, galaxy1.y)


def find_galaxies(universe: list[str]) -> list[UniverseLocation]:
    locations = []
    for y, row in enumerate(universe):
        for x, location in enumerate(row):
            if location == "#":
                locations += [UniverseLocation(x=x, y=y)]
    return locations


def part_one(universe: list[str], expansion_size=1) -> int:
    expanded = expand_universe(universe, expansion_size)
    galaxies = find_galaxies(expanded)
    total = 0
    for galaxy1, galaxy2 in combinations(galaxies,2):
        total += galaxy_distance(galaxy1, galaxy2)
    return total


def part_two(universe: list[str], expansion_size: int) -> int:
    expansion_delta = part_one(universe, 2) - part_one(universe, 1)
    return part_one(universe) + (expansion_size-2) * expansion_delta


def main():
    universe = load_galaxy("input/d11.txt")
    print(part_one(universe))
    print(part_two(universe, 1000000))


if __name__ == "__main__":
    main()
