import copy
from typing import List
from tools.file_loader import load_string_groups
from dataclasses import dataclass
from math import inf


class Unhandled(Exception):
    pass


@dataclass
class Vector:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


@dataclass
class DirectedVector(Vector):
    """
    Obviously this is a naming mishap - a vector has direction. Mistakes were made in Part 1...
    """
    x_start: int
    x_end: int
    y_start: int
    y_end: int


def promote_vector(vector: Vector) -> DirectedVector:
    if vector.x_min != vector.x_max and vector.y_min != vector.y_max:
        raise Unhandled

    return DirectedVector(
        x_min = vector.x_min,
        x_max = vector.x_max,
        y_min=vector.y_min,
        y_max=vector.y_max,
        x_start=vector.x_min,
        x_end=vector.x_max,
        y_start=vector.y_min,
        y_end=vector.y_max)


def promote_point(x: int, y: int):
    return DirectedVector(
        x_min = x,
        x_max = x,
        y_min=y,
        y_max=y,
        x_start=x,
        x_end=x,
        y_start=y,
        y_end=y)


def promote_line(start_x, start_y, end_x, end_y):
    return DirectedVector(
        x_min = min(start_x, end_x),
        x_max = max(start_x, end_x),
        y_min=min(start_y, end_y),
        y_max=max(start_y, end_y),
        x_start=start_x,
        x_end=end_x,
        y_start=start_y,
        y_end=end_y)



def point_count(vector: Vector):
    if vector.x_max == vector.x_min:
        length = 1 + vector.y_max - vector.y_min
    elif vector.y_min == vector.y_max:
        length = 1 + vector.x_max - vector.x_min
    elif (vector.x_max - vector.x_min) == (vector.y_max - vector.y_min):
        length = 1 + (vector.x_max - vector.x_min)
    else:
        raise Unhandled

    return length


def parse_vector(code: str) -> DirectedVector:
    start, end = [[int(x) for x in coord.split(",")] for coord in code.split("->")]
    return DirectedVector(x_max=max(start[0], end[0]),
                          x_min=min(start[0], end[0]),
                          y_min=min(start[1], end[1]),
                          y_max=max(start[1], end[1]),
                          x_start=start[0], x_end=end[0],
                          y_start=start[1], y_end=end[1])


def load_part_one(path: str) -> List[Vector]:
    with open(path, encoding="ascii") as file:
        vectors = [parse_vector(line) for line in file.readlines()]
    filtered_vectors = [vector for vector in vectors if vector.x_min == vector.x_max or vector.y_min == vector.y_max]
    return filtered_vectors


def load_part_two(path: str) -> List[Vector]:
    with open(path, encoding="ascii") as file:
        vectors = [parse_vector(line) for line in file.readlines()]
    return vectors


def check_overlap(a_min, a_max, b_min, b_max):
    return (b_min <= a_min <= b_max) or (a_min <= b_min <= a_max)

def vector_gradient(vector: DirectedVector):
    if vector.x_start == vector.x_end:
        return inf
    return (vector.y_end - vector.y_start) / (vector.x_end - vector.x_start)


def get_intersection(first: DirectedVector, second: DirectedVector) -> List[DirectedVector]:
    intersections = []
    if check_overlap(first.x_min, first.x_max, second.x_min, second.x_max) and \
            check_overlap(first.y_min, first.y_max, second.y_min, second.y_max):
        if (first.x_min == first.x_max or first.y_min == first.y_max) and \
           (second.x_min == second.x_max or second.y_min == second.y_max):
            x_coords = [first.x_min, first.x_max, second.x_min, second.x_max]
            y_coords = [first.y_min, first.y_max, second.y_min, second.y_max]
            x_coord = max(set(x_coords), key=x_coords.count)
            y_coord = max(set(y_coords), key=y_coords.count)
            intersections.append(
                DirectedVector(x_min=x_coord, x_max=x_coord, y_min=y_coord, y_max=y_coord,
                               x_start=x_coord, x_end=x_coord, y_start=y_coord, y_end=y_coord))
        else:
            # y1 = mx + b
            m = vector_gradient(first)
            b = first.y_start - m * first.x_start
            # y2 = nx + c
            n = vector_gradient(second)
            c = second.y_start - n * second.x_start
            if m == inf:
                # first line is a vertical line
                x = first.x_min
                y = n*x + c
            elif n == inf:
                # second line is a vertical line
                x = second.x_min
                y = m*x + b
            else:
                # mx + b = nx + c => x(m-n) = c -b => x = (c-b) / (m-n)
                x = (c - b) / (m - n)
                y = m*x + b
            if first.x_min <= x <= first.x_max and second.x_min <= x <= second.x_max and \
               first.y_min <= y <= first.y_max and second.y_min <= y <= second.y_max:
                       intersections.append(promote_point(x, y))

    return intersections


def get_vector_overlap(first: DirectedVector, second: DirectedVector) -> List[DirectedVector]:
    overlaps = []

    first_gradient = vector_gradient(first)
    second_gradient = vector_gradient(second)

    if first_gradient == second_gradient:
        if first_gradient == 0 or first_gradient == inf:
            if first.y_min == second.y_min and first.y_max == second.y_max:
                if check_overlap(first.x_min ,first.x_max, second.x_min, second.x_max):
                    overlaps.append(promote_vector(Vector(
                        y_min = first.y_min,
                        y_max = first.y_max,
                        x_min = max(first.x_min, second.x_min),
                        x_max = min(first.x_max, second.x_max)
                    )))
            elif first.x_min == second.x_min and first.x_max == second.x_max:
                if check_overlap(first.y_min, first.y_max, second.y_min, second.y_max):
                    overlaps.append(promote_vector(Vector(
                        x_min = first.x_min,
                        x_max = first.x_max,
                        y_min = max(first.y_min, second.y_min),
                        y_max = min(first.y_max, second.y_max)
                    )))
        elif check_overlap(first.x_min ,first.x_max, second.x_min, second.x_max):
            first_c = (first.y_start) - (first_gradient * first.x_start)
            second_c = (second.y_start) - (second_gradient * second.x_start)
            if first_c == second_c:
                x_min = max(first.x_min, second.x_min)
                x_max = min(first.x_max, second.x_max)
                y_min = max(first.y_min, second.y_min)
                y_max = min(first.y_max, second.y_max)
                x_start = x_min
                x_end = x_max
                if first_gradient > 0:
                    y_start = y_min
                    y_end = y_max
                else:
                    y_start = y_max
                    y_end = y_min
                overlaps.append(DirectedVector(
                    x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                    x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end))
    else:
        overlaps += get_intersection(first, second)
    return overlaps


def get_all_overlaps(vectors: List[Vector]) -> List[Vector]:
    overlaps = []
    for i, vector in enumerate(vectors):
        for other_vector in vectors[i+1:]:
            overlaps += get_vector_overlap(vector, other_vector)
    return overlaps


def remove_overlap(vector: DirectedVector, reference: DirectedVector) -> List[Vector]:
    overlaps = get_vector_overlap(vector, reference)

    vectors = []
    if len(overlaps) == 1:
        overlap = overlaps[0]
        if vector.y_min == vector.y_max:
            if vector.x_min < overlap.x_min:
                vectors += [promote_vector(Vector(x_min=vector.x_min, x_max=overlap.x_min-1, y_min=vector.y_min, y_max=vector.y_max))]
            if vector.x_max > overlap.x_max:
                vectors += [promote_vector(Vector(x_min=overlap.x_max+1, x_max=vector.x_max, y_min=vector.y_min, y_max=vector.y_max))]
        elif vector.x_min == vector.x_max:
            if vector.y_min < overlap.y_min:
                vectors += [promote_vector(Vector(y_min=vector.y_min, y_max=overlap.y_min-1, x_min=vector.x_min, x_max=vector.x_max))]
            if vector.y_max > overlap.y_max:
                vectors += [promote_vector(Vector(y_min=overlap.y_max+1, y_max=vector.y_max, x_min=vector.x_min, x_max=vector.x_max))]
        else:
            gradient = vector_gradient(vector)
            if vector.x_start < overlap.x_start:
                start_x = vector.x_start
                start_y = vector.y_start
                end_x = overlap.x_start -1
                vectors += [promote_line(start_x, start_y, end_x, start_y + gradient * (end_x - start_x))]

            if vector.x_end > overlap.x_end:
                start_x = overlap.x_end +1
                end_x = vector.x_end
                end_y = vector.y_end
                start_y = end_y - gradient*(end_x - start_x)
                vectors += [promote_line(start_x, start_y, end_x, end_y)]
    elif len(overlaps) == 0:
        vectors = [vector]
    else:
        raise Unhandled

    return vectors


def remove_overlaps(vector: Vector, reference: List[Vector]) -> List[Vector]:
    stack = [vector]
    result = []
    while stack:
        for next_vector in reference:
            reduced = remove_overlap(vector, next_vector)
            if len(reduced) > 1:
                stack += reduced[1:]
            if reduced:
                vector = reduced[0]
            else:
                vector = None
                break
        if vector:
            result.append(vector)
        vector = stack.pop()

    return result


def remove_all_overlaps(vectors: List[Vector]):
    result = []
    for i, vector in enumerate(vectors):
        print ("{0} of {1}".format(i, len(vectors)))
        result += remove_overlaps(vector, vectors[i+1:])
    return result


def part_one(path: str) -> int:
    vectors = load_part_one(path)
    overlaps = get_all_overlaps(vectors)
    unique_overlaps = remove_all_overlaps(overlaps)
    count = 0
    for vector in unique_overlaps:
        count += point_count(vector)

    return count

def count_overlaps(path: str):
    vectors = load_part_two(path)
    print ("Loaded")
    print ("Got Overlaps")
    overlaps = get_all_overlaps(vectors)
    count = 0
    for vector in overlaps:
        count += point_count(vector)
    origin_count = 0
    for vector in vectors:
        origin_count += point_count(vector)
    print (count)
    print (origin_count / count)
    print (count_overlap(vectors))
    print (count_overlap(overlaps, 1))


def part_two_full(path: str) -> int:
    vectors = load_part_two(path)
    print ("Loaded")
    overlaps = get_all_overlaps(vectors)
    print ("Got Overlaps")
    unique_overlaps = remove_all_overlaps(overlaps)
    print ("GOt uniques")
    count = 0
    for vector in unique_overlaps:
        count += point_count(vector)
    return count

def count_overlap(vectors: List[DirectedVector], threshold=2):
    grid = {}
    for vector in vectors:
        gradient = vector_gradient(vector)
        if gradient == inf:
            x = vector.x_start
            for y in range(int(vector.y_min), int(vector.y_max)+1):
                key = "{0}:{1}".format(int(x),int(y))
                if key in grid:
                    grid[key] += 1
                else:
                    grid[key] = 1
        else:
            if vector.x_start > vector.x_end:
                y = vector.y_end
            else:
                y = vector.y_start
            for x in range(int(vector.x_min), int(vector.x_max)+1):
                key = "{0}:{1}".format(int(x),int(y))
                if key in grid:
                    grid[key] += 1
                else:
                    grid[key] = 1
                y += gradient
    count = 0
    for cell in grid:
        if grid[cell] >= threshold:
            count += 1
    return count

def part_two(path: str) -> int:
    vectors = load_part_two(path)
    return count_overlap(vectors)


def debug_draw(vectors: List[DirectedVector]):
    grid = {}
    for vector in vectors:
        gradient = vector_gradient(vector)
        if gradient == inf:
            x = vector.x_start
            for y in range(int(vector.y_min), int(vector.y_max)+1):
                key = "{0}:{1}".format(int(x),int(y))
                if key in grid:
                    grid[key] += 1
                else:
                    grid[key] = 1
        else:
            if vector.x_start > vector.x_end:
                y = vector.y_end
            else:
                y = vector.y_start
            for x in range(int(vector.x_min), int(vector.x_max)+1):
                key = "{0}:{1}".format(int(x),int(y))
                if key in grid:
                    grid[key] += 1
                else:
                    grid[key] = 1
                y += gradient

    for y in range(10):
        line = ""
        for x in range(10):
            key = "{0}:{1}".format(x,y)
            if key in grid:
                line += str(grid[key])
            else:
                line += "."
        print(line)
    print (grid)

if __name__ == "__main__":
    def main():
        print(part_two("input/d05.txt"))
        print(count_overlaps("input/d05.txt"))
    main()
