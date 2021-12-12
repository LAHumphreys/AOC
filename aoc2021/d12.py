from typing import List, Dict
from enum import Enum
from copy import copy


class CaveType(Enum):
    SMALL = "small"
    LARGE = "large"
    START = "start"
    END = "end"


class Unhandled(Exception):
    pass


def get_cave_type(cave: str) -> CaveType:
    if cave == "start":
        return CaveType.START
    if cave == "end":
        return CaveType.END
    if len(cave) == 1 and "a" <= cave <= "z":
        return CaveType.SMALL
    if len(cave) == 1 and "A" <= cave <= "Z":
        return CaveType.LARGE
    if len(cave) == 2:
        first_type, second_type = [get_cave_type(token) for token in cave]
        if first_type == second_type:
            return first_type
        raise Unhandled
    raise Unhandled


def load_map(path: str) -> Dict[str, List[str]]:
    with open(path, encoding="ascii") as file:
        routes = [line.replace("\n", "").split("-") for line in file.readlines()]
    cave_map: Dict[str, List[str]] = {}
    for start, end in routes:
        if start not in cave_map:
            cave_map[start] = [end]
        else:
            cave_map[start].append(end)

        if end not in cave_map:
            cave_map[end] = [start]
        else:
            cave_map[end].append(start)
    return cave_map


def get_repeat(path: List[str]) -> str:
    repeat = None
    small_caves = set()
    for previous_cave in path:
        if get_cave_type(previous_cave) == CaveType.SMALL:
            if previous_cave not in small_caves:
                small_caves.add(previous_cave)
            else:
                repeat = previous_cave
                break
    return repeat


def get_path_options(cave_map: Dict[str, List[str]],
                     path: List[str],
                     small_limit: int = 1) -> List[str]:
    current_cave = path[-1]
    if get_cave_type(current_cave) == CaveType.START:
        return cave_map[current_cave]
    if get_cave_type(current_cave) == CaveType.END:
        return []

    options = []
    for option in cave_map[current_cave]:
        option_type = get_cave_type(option)
        if option_type == CaveType.START:
            pass
        elif option_type in (CaveType.END, CaveType.LARGE):
            options.append(option)
        elif option_type == CaveType.SMALL and option not in path:
            options.append(option)
        elif option_type == CaveType.SMALL and small_limit == 1:
            pass
        elif option_type == CaveType.SMALL and small_limit == 2:
            repeat_cave = get_repeat(path)
            if not repeat_cave:
                options.append(option)
            else:
                # Can't add a new second cave
                pass
        else:
            raise Unhandled
    return options


def get_paths(cave_map: Dict[str, List[str]],
              current_path=None,
              small_limit: int = 1) -> List[List[str]]:
    if current_path is None:
        current_path = ["start"]

    paths = []
    options = get_path_options(cave_map, current_path, small_limit)
    for option in options:
        new_path = copy(current_path) + [option]
        if get_cave_type(option) == CaveType.END:
            paths.append(new_path)
        else:
            paths += get_paths(cave_map, new_path, small_limit)

    return paths


if __name__ == "__main__":
    def main():
        cave_map = load_map("input/d12.txt")
        paths = get_paths(cave_map)
        print(len(paths))
        paths = get_paths(cave_map, small_limit=2)
        print(len(paths))
    main()
