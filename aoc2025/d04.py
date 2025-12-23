def load_sample(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def count_rows(the_map: list[str]) -> list[list[int]]:
    individual_row_counts = [count_row(row) for row in the_map]
    row_len = len(the_map[0])
    empty_row = [0] * row_len
    counted_rows = []
    for row_index, row in enumerate(individual_row_counts):
        above = individual_row_counts[row_index-1] if row_index > 0 else empty_row
        below = individual_row_counts[row_index+1] if row_index < row_len-1 else empty_row
        counted_row = []
        for point_index, point in enumerate(the_map[row_index]):
            point_value = 0
            if point == "@":
                point_value = row[point_index] + above[point_index] + below[point_index]
            counted_row.append(point_value)
        counted_rows.append(counted_row)
    return counted_rows

def convert_map_point(point: str):
    if point == "@":
        return 1
    elif point == ".":
        return 0
    else:
        raise ValueError(f"Invalid map point: {point}")

def count_row(row: str) -> list[int]:
    index = -1
    point = 0
    rhs = convert_map_point(row[0])
    result = []
    while index < len(row) -1:
        index += 1
        lhs = point
        point = rhs
        if index < len(row)-1:
            rhs = convert_map_point(row[index+1])
        else:
            rhs = 0
        result.append(lhs + point + rhs)
    return result

def part1(data: list[str]) -> int:
    data = count_rows(data)
    total = 0
    for row in data:
        for point in row:
            if 0 < point <= 4:
                total += 1
    return total


def part2(data: list[str]) -> int:
    changed = True
    total = 0
    while changed:
        print("Updating Map:")
        for row in data:
            print(row)
        changed = False
        counted_data = count_rows(data)
        new_data = []
        for row_index, row in enumerate(counted_data):
            new_row = ""
            for point_index, point in enumerate(row):
                if 0 < point <= 4:
                    total += 1
                    new_row += "."
                    changed = True
                else:
                    new_row += data[row_index][point_index]
            new_data.append(new_row)
        data = new_data
    return total


def main():
    try:
        data = load_sample("input/d04.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
