from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Point:
    x: int
    y: int

def load_sample(file: str) -> list[Point]:
    with open(file, "r", encoding="utf-8") as f:
        return [Point(int(x), int(y)) for x, y in
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

def find_biggest_box_for_side(top: Point, points: list[Point], is_rhs: bool) -> int:
    points.sort(key=lambda p: p.y)
    max_size = 0
    for index, point in enumerate(points):
        size = calc_size(top, point)
        if size > max_size:
            valid = True
            for other in points[0:index]:
                if is_rhs:
                    if other.x <= point.x:
                        valid = False
                        break
                else:
                    if other.x >= point.x:
                        valid = False
                        break
            if valid:
                max_size = size
                print(f"New max size {max_size} at {point}")
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

    max_size = find_biggest_box_for_side(top, possible_rhs_points, True)
    lhs_max = find_biggest_box_for_side(top, possible_lhs_points, False)
    return max(max_size, lhs_max)

def get_scaled_coords(point: Point, min_x: int, min_y: int,
                      scalar_x: float, scalar_y: float) -> tuple[int, int]:
    x = int((point.x - min_x) * scalar_x)
    y = int((point.y - min_y) * scalar_y)
    return x, y

def draw_line(rows: list[str], start: tuple[int, int], end: tuple[int, int]):
    if start[0] == end[0]:  # Vertical line
        x = start[0]
        line_y = min(start[1], end[1]) + 1
        max_y = max(start[1], end[1])
        while line_y <= max_y and rows[line_y][x] == " ":
            rows[line_y] = rows[line_y][:x] + "|" + rows[line_y][x+1:]
            line_y += 1
    elif start[1] == end[1]:  # Horizontal line
        y = start[1]
        line_x = min(start[0], end[0]) + 1
        max_x = max(start[0], end[0])
        while line_x <= max_x and rows[y][line_x] == " ":
            rows[y] = rows[y][:line_x] + "-" + rows[y][line_x+1:]
            line_x += 1
    else:
        raise ValueError("Not a perpendicular line")

def get_grid_scalars(points: list[Point], grid_size: int) -> tuple:
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    scalar_x = (grid_size - 1) / (max_x - min_x)
    scalar_y = (grid_size - 1) / (max_y - min_y)
    return min_x, min_y, scalar_x, scalar_y

def print_grid(points: list[Point]):
    grid_size = 120
    min_x, min_y, scalar_x, scalar_y = get_grid_scalars(points, grid_size)

    rows = [" " * 114 + "X" + " " * (grid_size - 114) for _ in range(grid_size)]
    row_points: list[list[Point]] = [[] for _ in range(grid_size)]

    last_scaled: Optional[tuple[int, int]] = None
    for point in points:
        x, y = get_scaled_coords(point, min_x, min_y, scalar_x, scalar_y)
        rows[y] = rows[y][:x] + "#" + rows[y][x+1:]
        row_points[y].append(point)

        if last_scaled:
            draw_line(rows, last_scaled, (x, y))

        last_scaled = (x, y)

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
