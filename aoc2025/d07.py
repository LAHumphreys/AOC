from copy import deepcopy

def load_sample(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def display_paths(paths: list[str]) -> None:
    for path in paths:
        print(path)

def propagate_tachyon(paths: list[str], row_idx: int) -> int:
    num_splits = 0
    source_row = paths[row_idx-1]
    map_row = paths[row_idx]
    print(f"source row: {source_row}")
    print(f"map row:    {map_row}")
    new_row = ""
    skip_next = False
    for index, source_point in enumerate(source_row):
        if skip_next:
            skip_next = False
            continue
        map_point = map_row[index]
        if source_point == "|" or source_point == "S":
            # NOTE: The input never has two splitter next to each other
            #       note is a splitter ever on the edge
            if map_point == "^":
                num_splits += 1
                new_row = new_row[:-1]
                new_row += "|^|"
                skip_next = True
            else:
                new_row += "|"
        else:
            new_row += map_point
    paths[row_idx] = new_row
    return num_splits


def part1(data: list[str]) -> int:
    splits = 0
    display_paths(data)
    for i in range(1, len(data)):
        splits += propagate_tachyon(data, i)
    display_paths(data)
    return splits


def part2(data: list[str]) -> int:
    return len(data)


def main():
    try:
        data = load_sample("input/d07.txt")
        print(f"Part 1: {part1(deepcopy(data))}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
