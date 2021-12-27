from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Seabed:
    seabed: List[str]
    height: int
    width: int


def step_until_stop(seabed: Seabed) -> Tuple[int, Seabed]:
    steps = 0
    moved = -1
    while moved != 0:
        moved, seabed = _do_step(seabed)
        steps += 1
    return steps, seabed


def _do_step(seabed: Seabed) -> Tuple[int, Seabed]:
    moved = 0
    newbed: List[List[str]] = [["."]*seabed.width for _ in range(seabed.height)]
    # Eastward current
    for row_idx, row in enumerate(seabed.seabed):
        for col_idx, cell in enumerate(row):
            if cell == ">":
                new_col_idx = (col_idx + 1) % seabed.width
                next_space = seabed.seabed[row_idx][new_col_idx]
                if next_space == ".":
                    moved += 1
                    newbed[row_idx][new_col_idx] = ">"
                else:
                    newbed[row_idx][col_idx] = ">"


    # Southward current
    for row_idx, row in enumerate(seabed.seabed):
        for col_idx, cell in enumerate(row):
            if cell == "v":
                new_row_idx = (row_idx + 1) % seabed.height
                next_space = seabed.seabed[new_row_idx][col_idx]
                next_new_space = newbed[new_row_idx][col_idx]

                if next_space != "v" and next_new_space == ".":
                    moved += 1
                    newbed[new_row_idx][col_idx] = "v"
                else:
                    newbed[row_idx][col_idx] = "v"

    return moved, Seabed(seabed=["".join(row) for row in newbed],
                         height=seabed.height,
                         width=seabed.width)


def do_step(seabed: Seabed) -> Seabed:
    return _do_step(seabed)[1]


def load_seabed(path: str) -> Seabed:
    with open(path, encoding="ascii") as file:
        seabed = [line.rstrip() for line in file.readlines()]
    return Seabed(
        seabed=seabed,
        height=len(seabed),
        width=len(seabed[0])
    )

if __name__ == "__main__":
    def main():
        seabed = load_seabed("input/d25.txt")
        print(step_until_stop(seabed))
    main()
