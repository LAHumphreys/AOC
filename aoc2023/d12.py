from enum import Enum
from dataclasses import dataclass
from typing import Optional
from itertools import chain, tee
from copy import copy, deepcopy

@dataclass
class SpringMap:
    row: str
    groups: list[int]


def expand_spring(short: SpringMap) -> SpringMap:
    return SpringMap(row=((short.row+"?")*5)[:-1], groups=short.groups*5)


def load_springs(file_name: str) -> list[SpringMap]:
    with open(file_name) as input_file:
        result = []
        for line in (ln.replace("\n", "") for ln in input_file.readlines()):
            row, group_str = line.split()
            groups = [int(group) for group in group_str.split(",")]
            result += [SpringMap(row=row, groups=groups)]
        return result


def part_one(springs: list[SpringMap]) -> int:
    total = 0
    count = 0
    for spring in springs:
        total += sum(1 for _ in spring_possibilities(spring.row, spring.groups))
        count += 1
        print(f"{count}: {total}")
    return total


def part_two(springs: list[SpringMap]) -> int:
    total = 0
    count = 0
    for spring in (expand_spring(spring) for spring in springs):
        total += sum(1 for _ in spring_possibilities(spring.row, spring.groups))
        count += 1
        print(f"{count}: {total}")
    return total


def make_key(row: str, groups: list[int]):
    key = row + ":" + ",".join(str(x) for x in groups)
    return key


TRIM_CACHE: dict[str, list[int]] = {}


def trim_groups(slice: str, groups: list[int]) -> list[int]:
    key = make_key(slice, groups)
    if key in TRIM_CACHE:
        return TRIM_CACHE[key]
    start_idx = 0
    valid = True
    remaining_groups = deepcopy(groups)
    slice_len = len(slice)
    if "#" in slice:
        while valid and remaining_groups:
            group = remaining_groups.pop(0)
            search_string = "#" * group
            next_idx = slice.find(search_string, start_idx) + group
            if next_idx < slice_len and slice[next_idx] != ".":
                valid = False
            if next_idx < group or next_idx > slice_len:
                valid = False
            if not valid:
                remaining_groups = [group] + remaining_groups
            else:
                start_idx = next_idx

    if remaining_groups and (start_idx < slice_len -1 or len(remaining_groups) == len(groups)):
        i = 0
        while i < slice_len and slice[-1*(i+1)] == "#":
            i += 1
        remaining_groups[0] = remaining_groups[0] - i
        if remaining_groups[0] <= 0:
            remaining_groups = remaining_groups[1:]
    TRIM_CACHE[key] = remaining_groups
    return remaining_groups


def wrapped_possibilities(prefix: str, suffix: str, groups: list[int], cache: dict[str, list[str]]):
    for after in spring_possibilities(suffix, groups, cache):
        yield prefix + after


SMALL_ITEM_CACHE: dict[str, list[str]] = {}


def spring_possibilities(in_row: str, groups: list[int], cache: dict[str, list[str]] = None) -> str:
    if cache is None:
        cache = {}
    key = make_key(in_row, groups)
    if key in SMALL_ITEM_CACHE:
        for row in SMALL_ITEM_CACHE[key]:
            yield row
    elif key in cache:
        for row in cache[key]:
            yield row
    else:
        first_unknown = in_row.find("?")
        if first_unknown >= 0:
            slice_before = in_row[:first_unknown]
            slice_after = in_row[first_unknown+1:]
            row_gens = []
            for x in [".", "#"]:
                before = slice_before + x
                after_groups = trim_groups(before, groups)
                row_gens += [wrapped_possibilities(before, slice_after, after_groups, cache)]
            rows = chain(*row_gens)
        else:
            rows = [in_row]

        valid_rows = []
        for row in rows:
            start_idx = 0
            valid = True
            for group in groups:
                next_idx = row.find("#", start_idx) + group
                if next_idx < len(row) and row[next_idx] != ".":
                    valid = False
                    break
                elif next_idx - group < 0:
                    valid = False
                    break
                elif row[next_idx-group: next_idx] != "#"*group:
                    valid = False
                    break
                elif next_idx < group:
                    valid = False
                    break
                start_idx = next_idx
            if "#" in row[start_idx:]:
                valid = False
            if valid:
                valid_rows.append(row)
                yield row
        cache[key] = valid_rows
        if len(valid_rows) < 1000:
            SMALL_ITEM_CACHE[key] = valid_rows


def main():
    springs = load_springs("input/d12.txt")
    print(part_one(springs))
    print(part_two(springs))
    pass


if __name__ == "__main__":
    main()
