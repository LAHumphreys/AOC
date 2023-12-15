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
        total += count_possibilities(spring.row, spring.groups)
        count += 1
        print(f"{count}: {total}")
    return total


def part_two(springs: list[SpringMap]) -> int:
    total = 0
    count = 0
    for spring in (expand_spring(spring) for spring in springs):
        total += count_possibilities(spring.row, spring.groups)
        count += 1
        print(f"{count}: {total}")
    return total


def make_key(row: str, groups: list[int]):
    key = row + ":" + ",".join(str(x) for x in groups)
    return key


def subtract_groups(full_groups: list[int], trail_groups: list[int]):
    remainder = copy(full_groups)
    if not trail_groups:
        return remainder
    for i in range(len(trail_groups)-1):
        remainder.pop()
    if remainder[-1] == trail_groups[0]:
        remainder.pop()
    else:
        remainder[-1] -= trail_groups[0]
    return remainder


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


COUNT_CACHE: dict[str, int] = {}


def count_possibilities(in_row: str, groups: list[int]) -> int:
    key = make_key(in_row, groups)
    if key in COUNT_CACHE:
        return COUNT_CACHE[key]

    count = 0
    first_unknown = in_row.find("?")
    if first_unknown >= 0:
        slice_before = in_row[:first_unknown]
        slice_after = in_row[first_unknown+1:]
        for x in [".", "#"]:
            before = slice_before + x
            after_groups = trim_groups(before, groups)
            before_groups = subtract_groups(groups, after_groups)
            valid_split = True
            if x == "#":
                if not before_groups:
                    valid_split = False
                else:
                    if after_groups:
                        trail_group_len = after_groups[0]
                        marked_len = 1
                        prefix = ""
                        if before_groups[-1] != groups[len(before_groups)-1]:
                            while valid_split and marked_len <= trail_group_len:
                                if (marked_len-1) >= len(slice_after) or slice_after[marked_len-1] == ".":
                                    valid_split = False
                                else:
                                    prefix += "#"
                                marked_len += 1

                        if marked_len <= len(slice_after):
                            if slice_after[marked_len-1] == "#":
                                valid_split = False
                            else:
                                prefix += "."
                        slice_after = prefix + slice_after[len(prefix):]

            if valid_split:
                rhs_count = count_possibilities(slice_after, after_groups)
                # LHS couldbe invalid (so 1 or 0)
                lhs_count = count_possibilities(before, before_groups)
                #print(f"Count: {in_row}: {groups} => (+{x}) {before}: {before_groups} + {slice_after}: {after_groups} ({lhs_count*rhs_count})")
                count += lhs_count*rhs_count
    else:
        count = sum(1 for _ in spring_possibilities(in_row, groups))
    COUNT_CACHE[key] = count
    return count


def spring_possibilities(in_row: str, groups: list[int], cache: dict[str, list[str]] = None) -> str:
    key = make_key(in_row, groups)
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

    valid_rows = 0
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
            valid_rows += 1
            yield row
    COUNT_CACHE[key] = valid_rows


def main():
    springs = load_springs("input/d12.txt")
    print(part_one(springs))
    print(part_two(springs))
    pass


if __name__ == "__main__":
    main()
