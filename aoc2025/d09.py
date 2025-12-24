from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def load_sample(file: str) -> list[Point]:
    with open(file, "r", encoding="utf-8") as f:
        return [Point(int(x), int(y)) for x, y in\
                    (line.strip().split(",") for line in f.readlines())]



def part1(data: list[Point]) -> int:
    max_size = 0
    for index, point in enumerate(data):
        for other in data[index+1:]:
            size = (1 +abs(point.x - other.x)) * (1+abs(point.y - other.y))
            max_size = max(max_size, size)
    return max_size


def part2(data: list[Point]) -> int:
    return len(data)


def main():
    try:
        data = load_sample("input/d09.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
