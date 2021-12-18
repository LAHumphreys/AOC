from math import sqrt, ceil
from dataclasses import dataclass


def min_velocity_after(distance: int) -> int:
    # v * (v+1)/2 = D ==> 2*D = v^2 +v ==> V^2 + V -2*D = 0
    quad_b = 1
    quad_a = 1
    quad_c = -2 * distance
    return ceil((-1 * quad_b + sqrt(quad_b - 4 * quad_a * quad_c)) / 2 * quad_b)


@dataclass(frozen=True)
class Box:
    min_x: int
    max_x: int
    min_y: int
    max_y: int


def find_all(box: Box):
    min_x_v = min_velocity_after(box.min_x)
    max_x_v = box.max_x
    matches = []
    for x in range(min_x_v, max_x_v + 1):
        max_y_v = max(abs(box.min_y), 2 * x)
        y = -1 * max_y_v
        while y < max_y_v:
            if run_simulation(x, y, box)[0]:
                matches += [(x, y)]
            y += 1
    return matches


def run_simulation(x_v, y_v, box: Box):
    x = y = 0
    hit_box = False
    steps = 0
    while not hit_box and x <= box.max_x and y >= box.min_y:
        steps += 1
        x += x_v
        y += y_v
        if x_v > 0:
            x_v -= 1
        elif x_v < 0:
            x_v += 1

        if box.min_x <= x <= box.max_x and box.min_y <= y <= box.max_y:
            hit_box = True

        y_v -= 1
    return hit_box, steps


if __name__ == "__main__":
    def main():
        in_max_y: int = -148
        in_min_y: int = -189
        in_min_x: int = 48
        in_max_x: int = 70
        print(len(find_all(Box(in_min_x, in_max_x, in_min_y, in_max_y))))


    main()
