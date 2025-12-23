from dataclasses import dataclass

@dataclass
class MinMax:
    min: int
    max: int

@dataclass
class Inventory:
    ranges: list[MinMax]
    items: list[int]

    def __post_init__(self):
        if not self.ranges:
            return
        sorted_ranges = sorted(self.ranges, key=lambda r: r.min)
        self.ranges = [sorted_ranges[0]]
        for range_ in sorted_ranges[1:]:
            max_range = self.ranges[-1]
            if range_.min <= max_range.max:
                if range_.max > max_range.max:
                    self.ranges[-1].max = range_.max
            else:
                self.ranges.append(range_)

    def in_ranges(self, item: int):
        for range_ in self.ranges:
            if range_.min <= item <= range_.max:
                return True
            if range_.min > item:
                return False
        return False

def parse_range(range_str: str) -> MinMax:
    min_val, max_val = range_str.split("-")
    return MinMax(int(min_val), int(max_val))

def load_sample(file: str) -> Inventory:
    ranges: list[MinMax] = []
    items: list[int] = []
    with open(file, "r", encoding="utf-8") as f:
        for line in  (line.strip() for line in f.readlines()):
            if "-" in line:
                ranges.append(parse_range(line))
            elif line:
                items.append(int(line))
    return Inventory(ranges, items)


def part1(data: Inventory):
    count = 0
    for item in data.items:
        if data.in_ranges(item):
            count += 1

    return count


def part2(data: Inventory):
    count = 0
    for range_ in data.ranges:
        count += range_.max - range_.min + 1
    return count


def main():
    try:
        data = load_sample("input/d05.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
