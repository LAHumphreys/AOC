from dataclasses import dataclass


@dataclass
class Direction:
    x: int
    y: int


@dataclass
class Instruction:
    direction: Direction


def load_instructions(file_name: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    with open(file_name, encoding='utf-8') as input_file:
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


def _is_edge_boundary(
        ground: list[list[str]], x: int, y: int, max_x: int, max_y: int
) -> tuple[bool, bool]:
    """Check if position is at an edge boundary (right and below)."""
    rhs_is_empty = x == max_x - 1 or ground[y][x+1] != "#"
    below_is_empty = y == max_y - 1 or ground[y+1][x] != "#"
    return rhs_is_empty, below_is_empty


def _mark_boundaries_pass(
        ground: list[list[str]], max_x: int, max_y: int, reverse: bool = False
) -> None:
    """
    Perform boundary marking pass (forward or reverse).
    Forward pass marks outside cells with +, -, |
    Reverse pass cleans up and finalizes with spaces or dots.
    """
    num_edges_in_col = [0] * max_x
    row_iterator = reversed(list(enumerate(ground))) if reverse else enumerate(ground)

    for y, row in row_iterator:
        num_edges_in_row = 0
        col_iterator = reversed(list(enumerate(row))) if reverse else enumerate(row)

        for x, token in col_iterator:
            rhs_is_empty, below_is_empty = _is_edge_boundary(ground, x, y, max_x, max_y)

            # Count edges
            if token == "#":
                if rhs_is_empty:
                    num_edges_in_row += 1
                if below_is_empty:
                    num_edges_in_col[x] += 1

            # Mark cells based on edge counts
            edges_even = (num_edges_in_row % 2 == 0, num_edges_in_col[x] % 2 == 0)
            if reverse:
                _mark_cell_reverse_pass(ground, x, y, token, edges_even)
            else:
                _mark_cell_forward_pass(ground, x, y, token, edges_even)


def _mark_cell_forward_pass(
        ground: list[list[str]], x: int, y: int, token: str,
        edges_even: tuple[bool, bool]
) -> None:
    """Mark cell during forward pass."""
    if token != ".":
        return

    row_even, col_even = edges_even

    if row_even and col_even:
        ground[y][x] = "+"
    elif row_even:
        ground[y][x] = "-"
        print(f"Dash: {x}, {y}")
    elif col_even:
        ground[y][x] = "|"
    else:
        print(f"Valid: {x}, {y}")


def _mark_cell_reverse_pass(
        ground: list[list[str]], x: int, y: int, token: str,
        edges_even: tuple[bool, bool]
) -> None:
    """Mark cell during reverse pass."""
    if token not in ["-", "+", "|"]:
        return

    row_even, col_even = edges_even

    if (row_even and token in ["-", "+"]) or (col_even and token in ["|", "+"]):
        ground[y][x] = " "
    else:
        ground[y][x] = "."


def draw_trench(instructions: list[Instruction]) -> list[list[str]]:
    max_x, max_y, x, y = get_bounds(instructions)
    ground = [["." for _ in range(max_x)] for _ in range(max_y)]

    # Draw the trench edges
    for instruction in instructions:
        dx = int(instruction.direction.x / max(1, abs(instruction.direction.x)))
        dy = int(instruction.direction.y / max(1, abs(instruction.direction.y)))
        target_x = x + instruction.direction.x
        target_y = y + instruction.direction.y
        while x != target_x or y != target_y:
            x += dx
            y += dy
            ground[y][x] = "#"

    # Forward pass: mark boundaries from top-left
    _mark_boundaries_pass(ground, max_x, max_y, reverse=False)
    for row in ground:
        print("".join(row))

    # Reverse pass: clean up and finalize from bottom-right
    _mark_boundaries_pass(ground, max_x, max_y, reverse=True)
    for row in ground:
        print("".join(row))

    return ground





def main():
    instructions = load_instructions("input/d18.txt")
    print(get_bounds(instructions))
    draw_trench(instructions)


if __name__ == "__main__":
    main()
