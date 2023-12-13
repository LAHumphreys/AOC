from enum import Enum
from dataclasses import dataclass
from typing import Optional
from itertools import chain, tee
from copy import copy, deepcopy

@dataclass
class SpringMap:
    row: str
    groups: list[int]


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
        uniques = []
        for variation in spring_possibilities(spring.row, spring.groups):
            if variation not in uniques:
                uniques += [variation]
        total += len(uniques)
        count += 1
        print(f"{spring.row}, {spring.groups}: {uniques}")
        print(f"{count}: {total}")
    return total

def trim_groups(slice: str, groups: list[int]) -> list[int]:
    start_idx = 0
    valid = True
    remaining_groups = deepcopy(groups)
    slice_len = len(slice)
    if "#" in slice:
        while valid and remaining_groups:
            group = remaining_groups.pop(0)
            search_string = "#" * group
            next_idx = slice.find(search_string, start_idx) + group
            next_hash = slice.find("#", start_idx)
            if next_hash + group != next_idx:
                valid = False
            if next_idx < slice_len and slice[next_idx] != ".":
                valid = False
            if next_idx < group or next_idx > slice_len:
                valid = False
            if not valid:
                remaining_groups = [group] + remaining_groups
            if next_idx > start_idx:
                start_idx = next_idx

    if remaining_groups and (start_idx < slice_len -1 or len(remaining_groups) == len(groups)):
        i = 0
        while i < slice_len and slice[-1*(i+1)] == "#" :
            i+=1
        remaining_groups[0] = remaining_groups[0] -i
        if remaining_groups[0] <= 0:
            remaining_groups = remaining_groups[1:]
    return remaining_groups


def wrapped_possibilities(prefix: str, suffix: str, groups: list[int]):
    for after in spring_possibilities(suffix, groups):
        yield prefix + after


def spring_possibilities(in_row: str, groups: list[int]) -> str:

    first_unknown = in_row.find("?")
    if first_unknown >= 0:
        slice_before = in_row[:first_unknown]
        slice_after = in_row[first_unknown+1:]
        row_gens = []
        for x in [".", "#"]:
            before = slice_before + x
            after_groups = trim_groups(before, groups)
            row_gens += [wrapped_possibilities(before, slice_after, after_groups)]
        rows = chain(*row_gens)
    else:
        rows = [in_row]

    for row in rows:
        start_idx = 0
        valid = True
        for group in groups:
            search_string = "#"*group
            next_idx = row.find(search_string, start_idx) + group
            if next_idx < len(row) and row[next_idx] != ".":
                valid = False
                break
            if start_idx < 0 or next_idx < start_idx:
                valid = False
                break
            start_idx = next_idx
        if "#" in row[start_idx:]:
            valid = False
        if valid:
            yield row


def main():
    springs = load_springs("input/d12.txt")
    print(part_one(springs))
    pass


if __name__ == "__main__":
    main()
