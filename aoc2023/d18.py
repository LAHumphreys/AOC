from enum import Enum
from dataclasses import dataclass
from typing import Optional
from tools.file_loader import load_string_groups


@dataclass
class Direction:
    x: int
    y: int


@dataclass
class Instruction:
    direction: Direction


def load_instructions(file_name: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    with open(file_name) as input_file:
        for line in (ln.replace("\n", "") for ln in input_file.readlines()):
            direction, distance, _ = line.split()
            distance = int(distance)
            if direction == "R":
                instructions.append(Instruction(direction=Direction(x=distance, y=0)))
            elif direction == "L":
                instructions.append(Instruction(direction=Direction(x=-1*distance, y=0)))
            elif direction == "U":
                instructions.append(Instruction(direction=Direction(y=-1 * distance, x=0)))
            elif direction == "D":
                instructions.append(Instruction(direction=Direction(y=distance, x=0)))
    return instructions


def get_bounds(instructions: list[Instruction]) -> tuple[int, int, int, int]:
    min_x = max_x = min_y = max_y = 0
    x = y = 1
    for instruction in instructions:
        x += instruction.direction.x
        y += instruction.direction.y
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
    return 1 + max_x - min_x, 1 + max_y - min_y, 1 - min_x, 1 - min_y


def draw_trench(instructions: list[Instruction]) -> list[list[str]]:
    max_x, max_y, x, y = get_bounds(instructions)
    ground = [["." for _ in range(max_x)] for _ in range(max_y)]
    for instruction in instructions:
        dx = int(instruction.direction.x / max(1, abs(instruction.direction.x)))
        dy = int(instruction.direction.y / max(1, abs(instruction.direction.y)))
        target_x = x + instruction.direction.x
        target_y = y + instruction.direction.y
        while x != target_x or y != target_y:
            x += dx
            y += dy
            ground[y][x] = "#"
    # Walk in from the left and the top, and mark ? anything that is out of bounds
    # without considering right/ bottom
    num_edges_in_col = [0] * max_y
    for y, row in enumerate(ground):
        num_edges_in_row = 0
        for x, token in enumerate(row):
            rhs_is_empty = x == max_x - 1 or ground[y][x+1] != "#"
            below_is_empty = y == max_y - 1 or ground[y+1][x] != "#"
            if token == "#" and rhs_is_empty:
                num_edges_in_row += 1
            if token == "#" and below_is_empty:
                num_edges_in_col[x] += 1
            if token == "." and (num_edges_in_row % 2 == 0 and num_edges_in_col[x] % 2 == 0):
                ground[y][x] = "+"
            elif token == "." and num_edges_in_row % 2 == 0:
                ground[y][x] = "-"
                print(f"Dash: {x}, {y}")
            elif token == "." and num_edges_in_col[x] % 2 == 0:
                ground[y][x] = "|"
            elif token == ".":
                print(f"Valid: {x}, {y}")
    for row in ground:
        print("".join(row))
    # Walk in from the right / bottom and knock out anything that's still out of bounds
    # clear the ? flag for anything in bounds
    num_edges_in_col = [0] * max_y
    for y, row in reversed([pair for pair in enumerate(ground)]):
        num_edges_in_row = 0
        for x, token in reversed([pair for pair in enumerate(row)]):
            rhs_is_empty = x == max_x - 1 or ground[y][x+1] != "#"
            below_is_empty = y == max_y - 1 or ground[y+1][x] != "#"
            if token == "#" and rhs_is_empty:
                num_edges_in_row += 1
            if token == "#" and below_is_empty:
                num_edges_in_col[x] += 1
            if num_edges_in_row % 2 == 0 and token in ["-", "+"]:
                ground[y][x] = " "
            elif num_edges_in_col[x] % 2 == 0 and token in ["|", "+"]:
                ground[y][x] = " "
            elif token in ["-", "+", "|"]:
                ground[y][x] = "."
    for row in ground:
        print("".join(row))
    return ground





def main():
    instructions = load_instructions("input/d18.txt")
    print(get_bounds(instructions))
    draw_trench(instructions)
    pass


if __name__ == "__main__":
    main()
