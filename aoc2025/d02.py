def load_sample(file: str) -> list[tuple[str, str]]:
    data = []
    with open(file, "r") as f:
        pairs = [line.strip() for line in f.readlines()][0].split(",")
        for pair in pairs:
            start, end = pair.split("-")
            data.append((start, end))
    return data

def is_invalid(digits: str) -> bool:
    invalid = False
    if len(digits) %2 == 0:
        split_idx = len(digits)//2
        invalid = (digits[:split_idx] == digits[split_idx:])
    return invalid

def get_next_repeat(digits: str) -> str:
    if len(digits) %2 != 0:
        return get_next_repeat("1" + "0"*len(digits))
    base = digits[:len(digits)//2]
    rhs = digits[len(digits)//2:]
    if rhs < base:
        return base*2
    return str(int(base) +1)*2

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


def part1(data: list[tuple[str, str]]) -> int:
    total = 0
    for start, end in data:
        total += sum(get_invalid_ids(start, end))
    return total

def part2(lines: list[str]) -> int:
    return 0

def main():
    try:
        data = load_sample("input/d02.txt")
        print(f"Part 1: {part1(data)}")
    except FileNotFoundError:
        print("Input file not found.")

if __name__ == "__main__":
    main()
