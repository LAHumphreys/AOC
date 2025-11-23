from dataclasses import dataclass

from tools.file_loader import load_string_groups


@dataclass
class SupplyStacks:
    stacks: dict[int, list[str]]


@dataclass
class Instruction:
    source: int
    destination: int
    count: int


def load_stacks(path: str) -> tuple[SupplyStacks, list[Instruction]]:
    def get_stacks(lines: list[str]) -> dict[int, list[str]]:
        col_map = {int(col): i for i, col in enumerate(lines[-1]) if col != ' '}

        stacks = {label: [] for label in col_map}
        for stack_line in reversed(stack_lines[:-1]):
            for label, col in col_map.items():
                if stack_line[col] != ' ':
                    stacks[label].append(stack_line[col])
        return stacks

    def get_instruction(line: str):
        _, count, _, source, _, destination = line.split()
        return Instruction(count=int(count),
                           source=int(source),
                           destination=int(destination))

    stack_lines, instructions = load_string_groups(path)
    return SupplyStacks(stacks=get_stacks(stack_lines)), \
           list(map(get_instruction, instructions))


# Part 1
def move_stack(instruction: Instruction, stacks: SupplyStacks):
    # N is small enough we can just be explicit, even
    # if this is somewhat inefficient in terms of interacting
    # with the python data structure.
    for _ in range(instruction.count):
        stacks.stacks[instruction.destination].append(
            stacks.stacks[instruction.source].pop()
        )


# Part 2
def move_full_stack(instruction: Instruction, stacks: SupplyStacks):
    source = stacks.stacks[instruction.source]
    destination = stacks.stacks[instruction.destination]

    destination += source[-1 * instruction.count:]
    del source[-1 * instruction.count:]


def get_code(stacks: SupplyStacks) -> str:
    return "".join([stack[-1] for stack in stacks.stacks.values()])


if __name__ == "__main__":
    def main():
        stacks, instructions = load_stacks("input/d05.txt")
        for instruction in instructions:
            move_stack(instruction, stacks)
        print(get_code(stacks))

        stacks, instructions = load_stacks("input/d05.txt")
        for instruction in instructions:
            move_full_stack(instruction, stacks)
        print(get_code(stacks))


    main()
