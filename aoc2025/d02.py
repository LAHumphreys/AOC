from typing import Optional
from tools.string_operations import subdivide


def load_sample(file: str) -> list[tuple[str, str]]:
    data = []
    with open(file, "r", encoding="utf-8") as f:
        pairs = [line.strip() for line in f.readlines()][0].split(",")
        for pair in pairs:
            start, end = pair.split("-")
            data.append((start, end))
    return data

def is_invalid(digits: str, group_size: Optional[int] = None) -> bool:
    if group_size is None:
        if len(digits) % 2 == 0:
            group_size = len(digits)//2
        else:
            return False

    invalid = False
    if len(digits) % group_size == 0:
        parts = subdivide(digits, group_size)
        base = parts.pop(0)
        invalid = all(base == part for part in parts)
    return invalid

def is_invalid_part_2(digits: str) -> bool:
    for group_size in range(len(digits)//2, 0, -1):
        if is_invalid(digits, group_size):
            return True
    return False

def get_next_repeat(digits: str) -> str:
    if len(digits) %2 != 0:
        return get_next_repeat("1" + "0"*len(digits))
    base = digits[:len(digits)//2]
    rhs = digits[len(digits)//2:]
    if rhs < base:
        return base*2
    return str(int(base) +1)*2

def get_first_invalid_of_len(str_len: int) -> str:
    for group_size in range(str_len // 2, 0, -1):
        if str_len % group_size == 0:
            base = "1" + "0"*(group_size-1)
            return base*(str_len//group_size)
    return "1"*str_len


def get_next_repeat_part_2(digits: str) -> str:
    str_len = len(digits)
    next_groups: list[int] = [int(get_first_invalid_of_len(str_len+1))]
    for group_size in range(str_len // 2, 0, -1):
        if str_len % group_size != 0:
            continue
        parts = subdivide(digits, group_size)
        num_parts = len(parts)
        base = parts.pop(0)
        base_repeat = int(base*num_parts)
        if base_repeat > int(digits):
            next_groups.append(base_repeat)
        else:
            next_groups.append(int(str(int(base)+1)*num_parts))
    return str(min(next_groups))


def get_invalid_ids(start: str, end: str) -> list[int]:
    invalid_ids = []
    working = start
    while int(working) < int(end):
        if is_invalid(working):
            invalid_ids.append(working)
        working = get_next_repeat(working)
    if is_invalid(end):
        invalid_ids.append(end)
    return [int(x) for x in invalid_ids]

def get_invalid_ids_part_2(start: str, end: str) -> list[int]:
    invalid_ids = []
    working = start
    while int(working) < int(end):
        if is_invalid_part_2(working):
            invalid_ids.append(working)
        working = get_next_repeat_part_2(working)
    if is_invalid_part_2(end):
        invalid_ids.append(end)
    return [int(x) for x in invalid_ids]


def part1(data: list[tuple[str, str]]) -> int:
    total = 0
    for start, end in data:
        total += sum(get_invalid_ids(start, end))
    return total

def part2(data: list[tuple[str, str]]) -> int:
    total = 0
    for start, end in data:
        total += sum(get_invalid_ids_part_2(start, end))
    return total

def main():
    try:
        data = load_sample("input/d02.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 1: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")

if __name__ == "__main__":
    main()
