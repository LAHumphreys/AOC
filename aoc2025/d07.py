from copy import deepcopy

def load_sample(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def display_paths(paths: list[str]) -> None:
    for path in paths:
        print(path)

def convert_start_row_to_worlds(start_row: str) -> list[int]:
    result = []
    for x in start_row:
        if x == "S":
            result.append(1)
        else:
            result.append(0)
    return result


def quantum_propagate_tachyon(source_row: list[int], map_row: str) -> list[int]:
    print(f"source row: {source_row}")
    print(f"map row:    {map_row}")
    new_row = [0] * len(source_row)
    for index, source_world_count in enumerate(source_row):
        map_point = map_row[index]
        if source_world_count > 0:
            # NOTE: The input never has two splitter next to each other
            #       note is a splitter ever on the edge
            if map_point == "^":
                new_row[index-1] += source_world_count
                new_row[index+1] += source_world_count
            else:
                new_row[index] += source_world_count
    return new_row

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
    display_paths(data)
    path = convert_start_row_to_worlds(data[0])
    for i in range(1, len(data)):
        print(path)
        path = quantum_propagate_tachyon(path, data[i])
    display_paths(data)
    print(path)
    return sum(path)


def main():
    try:
        data = load_sample("input/d07.txt")
        print(f"Part 1: {part1(deepcopy(data))}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
