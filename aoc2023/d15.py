from enum import Enum
from dataclasses import dataclass
from typing import Optional


def quick_hash(string:str) -> int:
    h = 0
    for c in string:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


def part_one(tokens: list[str]) -> int:
    return sum(quick_hash(t) for t in tokens)

def load_tokens(file_name: str) -> list[str]:
    with open(file_name, encoding='utf-8') as input_file:
        return input_file.read().split(",")


class Operation(Enum):
    REMOVE = "-"
    ADD = "="


@dataclass
class Instruction:
    operation: Operation
    box_no: int
    lense: str
    focal_length: Optional[int]


@dataclass
class Lense:
    label: str
    focal_length: int


def new_boxes() -> list[list[Lense]]:
    return [[] for _ in range(256)]


def apply_instruction(boxes: list[list[Lense]], instructions: list[Instruction]):
    for instruction in instructions:
        if instruction.operation == Operation.ADD:
            found = False
            for lense in boxes[instruction.box_no]:
                if lense.label == instruction.lense:
                    found = True
                    lense.focal_length = instruction.focal_length
            if not found:
                lense = Lense(label=instruction.lense, focal_length=instruction.focal_length)
                boxes[instruction.box_no].append(lense)
        else:
            boxes[instruction.box_no] = [box for box in boxes[instruction.box_no]
                                          if box.label != instruction.lense]

def parse_instruction(token: str) -> Instruction:
    if "-" in token:
        label = token.split("-")[0]
        return Instruction(
            operation=Operation.REMOVE,
            box_no=quick_hash(label),
            lense=label,
            focal_length=None
        )
    label, length = token.split("=")
    return Instruction(
            operation=Operation.ADD,
            box_no=quick_hash(label),
            lense=label,
            focal_length=int(length)
        )


def part_two(tokens: list[str]):
    instructions = [parse_instruction(token) for token in tokens]
    boxes = new_boxes()
    apply_instruction(boxes, instructions)
    total = 0
    for box_no, box in enumerate(boxes):
        for lense_no, lense in enumerate(box):
            focal_power = (box_no + 1) * (lense_no + 1) * lense.focal_length
            print(f"{focal_power}: {lense}")
            total += focal_power
    return total

def main():
    tokens = load_tokens("input/d15.txt")
    print(part_one(tokens))
    print(part_two(tokens))


if __name__ == "__main__":
    main()
