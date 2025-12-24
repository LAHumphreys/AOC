from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def load_sample(file: str) -> list[Point]:
    with open(file, "r", encoding="utf-8") as f:
        return [Point(int(x), int(y)) for x, y in\
                    (line.strip().split(",") for line in f.readlines())]

def calc_size(point1: Point, point2: Point) -> int:
    return (1 + abs(point1.x - point2.x)) * (1 + abs(point1.y - point2.y))

def part1(data: list[Point]) -> int:
    max_size = 0
    for index, point in enumerate(data):
        for other in data[index+1:]:
            size = calc_size(point, other)
            max_size = max(max_size, size)
    return max_size

def find_biggest_box(top: Point, other_points: list[Point]) -> int:
    """
    This misses all kinds of corner cases, but by inspection of the
    provided shape this is sufficient to get us the answer
    """
    if top not in other_points:
        raise ValueError("Top point not in point set!")
    possible_lhs_points: list[Point] = []
    possible_rhs_points: list[Point] = []
    for point in other_points:
        if point.y >  top.y:
            if point.x < top.x:
                possible_lhs_points.append(point)
            elif point.x > top.x:
                possible_rhs_points.append(point)
    possible_rhs_points.sort(key=lambda p: p.y)
    possible_lhs_points.sort(key=lambda p: p.y)
    max_size = 0
    for index, point in enumerate(possible_rhs_points):
        size = calc_size(top, point)
        if size > max_size:
            valid = True
            for other in possible_rhs_points[0:index]:
                if other.x <= point.x:
                    valid = False
                    break
            if valid:
                max_size = size
                print (f"New max size {max_size} at {point}")

    for index, point in enumerate(possible_lhs_points):
        size = calc_size(top, point)
        if size > max_size:
            valid = True
            for other in possible_lhs_points[0:index]:
                if other.x >= point.x:
                    valid = False
                    break
            if valid:
                max_size = size
                print (f"New max size {max_size} at {point}")
    return max_size

def print_grid(points: list[Point]):
    grid_size = 120
    max_x = max(points, key=lambda p: p.x).x
    max_y = max(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    scalar_x = (grid_size-1) / (max_x - min_x)
    scalar_y = (grid_size-1) / (max_y - min_y)
    rows = []
    row_points = []
    for i in range(grid_size):
        rows.append(" "*114 + "X" + " "*(grid_size-114))
        row_points.append([])
    last: Optional[tuple[int, int]] = None
    last_point: Optional[Point] = None
    for point in points:
        x = int((point.x - min_x) * scalar_x)
        y = int((point.y - min_y) * scalar_y)
        rows[y] = rows[y][0:x] + "#" + rows[y][x+1:]
        row_points[y].append(point)
        if last:
            if last[0] == x:
                line_y = min(last[1], y) +1
                end_y = max(last[1], y)
                if end_y - line_y > 20:
                    print(f"Large line: {x, line_y} -> {x, end_y}")
                    print(f"   From points: {point.x, point.y} -> {last_point.x, last_point.y}")
                while line_y <= end_y and rows[line_y][x] == " ":
                    rows[line_y] = rows[line_y][0:x] + "|" + rows[line_y][x+1:]
                    line_y += 1
            elif last[1] == y:
                line_x = min(last[0], x) +1
                end_x = max(last[0], x)
                if end_x - line_x > 20:
                    print(f"Large line: {line_x, y} -> {end_x, y}")
                    print(f"   From points: {point.x, point.y} -> {last_point.x, last_point.y}")
                while line_x <= end_x and rows[y][line_x] == " ":
                    rows[y] = rows[y][0:line_x] + "-" + rows[y][line_x+1:]
                    line_x += 1
            else:
                raise ValueError("Not a perpendicular line")
        last = (x, y)
        last_point = point
    for y, row in enumerate(rows):
        label = f"  : {y}"
        points_in_row = sorted(row_points[y], key=lambda p: p.x)
        for point in points_in_row:
            label += f", ({point.x}, {point.y})"
        print(row + label)



def main():
    try:
        data = load_sample("input/d09.txt")
        print(f"Part 1: {part1(data)}")
        print_grid(data)
        print(find_biggest_box(Point(x=94525, y=50422), data))
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
