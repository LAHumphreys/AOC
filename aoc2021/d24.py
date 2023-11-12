from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from sys import argv


class Unhandled(Exception):
    pass


@dataclass
class Registers:
    reg_w: int = None
    reg_x: int = None
    reg_y: int = None
    reg_z: int = None


def set_register(registers: Registers, register: str, value: int):
    if register == "w":
        registers.reg_w = value
    elif register == "x":
        registers.reg_x = value
    elif register == "y":
        registers.reg_y = value
    elif register == "z":
        registers.reg_z = value
    else:
        raise Unhandled


class InstructionType(Enum):
    INPUT = "inp"
    ADD = "add"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    EQUALS = "eql"
    SET = "_set"


@dataclass
class Instruction:
    target_register: str
    source_register: Optional[str]
    source_value: Optional[int]
    type: InstructionType


def decode(code: str) -> Instruction:
    tokens = code.split()
    inst_type = InstructionType(tokens[0])
    value = None
    source = None
    if inst_type != InstructionType.INPUT:
        source = tokens[2]
        if source not in ("w", "x", "y", "z"):
            value = int(source)
            source = None
    instruction = Instruction(
        target_register=tokens[1],
        source_register=source,
        source_value=value,
        type=inst_type)
    expand_instruction(instruction)
    return instruction


def expand_instruction(instruction: Instruction):
    if instruction.type == InstructionType.MUL:
        if instruction.source_value is not None and instruction.source_value == 0:
            instruction.type = InstructionType.SET
    elif instruction.type == InstructionType.MOD:
        if instruction.source_register is not None and \
                instruction.source_register == instruction.target_register:
            instruction.source_register = None
            instruction.source_value = 0
            instruction.type = InstructionType.SET
    elif instruction.type == InstructionType.DIV:
        if instruction.source_register is not None and \
                instruction.source_register == instruction.target_register:
            instruction.source_register = None
            instruction.source_value = 1
            instruction.type = InstructionType.SET
    elif instruction.type == InstructionType.EQUALS:
        if instruction.source_register is not None and \
                instruction.source_register == instruction.target_register:
            instruction.source_register = None
            instruction.source_value = 1
            instruction.type = InstructionType.SET


@dataclass
class BoundedValue:
    min: int
    max: int


@dataclass
class DependencyRegister:
    values: BoundedValue
    inputs: List[int]


@dataclass
class DependencyRegisters:
    reg_w: DependencyRegister
    reg_x: DependencyRegister
    reg_y: DependencyRegister
    reg_z: DependencyRegister


def track_dependencies(program: List[Instruction],
                       inputs: List[BoundedValue] = None) -> DependencyRegisters:
    if inputs is None:
        inputs = [BoundedValue(min=1, max=9)]*14
    registers: Dict[str, DependencyRegister] = {
        "w": DependencyRegister(BoundedValue(0, 0), []),
        "x": DependencyRegister(BoundedValue(0, 0), []),
        "y": DependencyRegister(BoundedValue(0, 0), []),
        "z": DependencyRegister(BoundedValue(0, 0), []),
    }
    input_count = 0
    for instruction in program:
        if instruction.type == InstructionType.INPUT:
            register = registers[instruction.target_register]
            register.inputs = [input_count]
            register.values.min = inputs[input_count].min
            register.values.max = inputs[input_count].max
            input_count += 1
        elif instruction.type == InstructionType.SET:
            register = registers[instruction.target_register]
            register.inputs = []
            register.values.min = instruction.source_value
            register.values.max = instruction.source_value
        else:
            if instruction.source_register is not None:
                rhs_values = registers[instruction.source_register].values
            else:
                rhs_values = BoundedValue(min=instruction.source_value,
                                          max=instruction.source_value)
            register = registers[instruction.target_register]
            apply_bounded_instruction(register.values, rhs_values, instruction.type)
            if register.values.min == register.values.max:
                register.inputs = []
            elif instruction.source_register is not None:
                for input_value in registers[instruction.source_register].inputs:
                    if input_value not in register.inputs:
                        register.inputs.append(input_value)

    return DependencyRegisters(reg_w=registers["w"],
                               reg_x=registers["x"],
                               reg_y=registers["y"],
                               reg_z=registers["z"], )


def reduce_bounds(program: List[Instruction], upper_bounds: List[int]) -> List[int]:
    inputs = []
    for i in range(len(upper_bounds)):
        inputs.append(BoundedValue(min=1, max=9))
    working_input = 0
    while working_input < len(inputs):
        matched = False
        max_value = upper_bounds[working_input]
        inputs[working_input] = BoundedValue(min=max_value, max=max_value)
        while not matched:
            registers = track_dependencies(program, inputs)
            if registers.reg_z.values.min <= 0 <= registers.reg_z.values.max:
                upper_bounds[working_input] = inputs[working_input].max
                matched = True
            else:
                inputs[working_input].min -= 1
                inputs[working_input].max -= 1
            if inputs[working_input].min < 1:
                print(f"Got stuck at {working_input}")
                backtrack_index = working_input - 1
                while upper_bounds[backtrack_index] == 1:
                    backtrack_index -= 1
                upper_bounds[backtrack_index] -= 1
                for i in range(backtrack_index + 1, len(upper_bounds)):
                    upper_bounds[i] = 9
                    inputs[i].min = 1
                    inputs[i].max = 9
                working_input = backtrack_index
                print(f"I'm back tracking to {working_input}")
                print(upper_bounds)
                working_input -= 1
                if working_input < -1:
                    raise Unhandled
                break
        working_input += 1
    return [bound.min for bound in inputs]


def reduce_bounds_from_below(program: List[Instruction], lower_bounds: List[int]) -> List[int]:
    inputs = []
    for i in range(len(lower_bounds)):
        inputs.append(BoundedValue(min=1, max=9))
    working_input = 0
    while working_input < len(inputs):
        matched = False
        min_value = lower_bounds[working_input]
        inputs[working_input] = BoundedValue(min=min_value, max=min_value)
        while not matched:
            registers = track_dependencies(program, inputs)
            if registers.reg_z.values.min <= 0 <= registers.reg_z.values.max:
                lower_bounds[working_input] = inputs[working_input].min
                matched = True
            else:
                inputs[working_input].min += 1
                inputs[working_input].max += 1
            if inputs[working_input].max > 9:
                print(f"Got stuck at {working_input}")
                backtrack_index = working_input - 1
                while lower_bounds[backtrack_index] == 9:
                    backtrack_index -= 1
                lower_bounds[backtrack_index] += 1
                for i in range(backtrack_index + 1, len(lower_bounds)):
                    lower_bounds[i] = 1
                    inputs[i].min = 1
                    inputs[i].max = 9
                working_input = backtrack_index
                print(f"I'm back tracking to {working_input}")
                print(lower_bounds)
                working_input -= 1
                if working_input < -1:
                    raise Unhandled
                break
        working_input += 1
    return [bound.min for bound in inputs]


def display_add_register(display: str, register: DependencyRegister, name: str):
    display += f"     {name}: "
    if register.values.min == register.values.max:
        display += f" {register.values.min:12d}                "
    else:
        display += f" {register.values.min:12d} -> {register.values.max:<12d}"

    if register.inputs:
        display += f" [{register.inputs[0]}"
        for input_value in register.inputs[1:]:
            display += f", {input_value}"
        display += "]"
    return display + "\n"


def display_registers(registers: DependencyRegisters):
    display = display_add_register("", registers.reg_w, "w")
    display = display_add_register(display, registers.reg_x, "x")
    display = display_add_register(display, registers.reg_y, "y")
    display = display_add_register(display, registers.reg_z, "z")

    return display


def debug_dump(path: str, inputs=None):
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    instructions = [decode(line) for line in lines]
    for i, line in enumerate(lines):
        print(line)
        registers = track_dependencies(instructions[0:i + 1], inputs)
        print(display_registers(registers))


def apply_bounded_instruction(target: BoundedValue, source: BoundedValue, i_type: InstructionType):
    if i_type == InstructionType.ADD:
        target.min += source.min
        target.max += source.max
    elif i_type == InstructionType.DIV:
        new_max = int(target.max / source.min)
        new_min = int(target.min / source.max)
        neg_min = int(target.min / source.min)
        neg_max = int(target.max / source.max)
        target.max = max(new_max, new_min, neg_min, neg_max)
        target.min = min(new_min, new_max, neg_min, neg_max)
    elif i_type == InstructionType.EQUALS:
        if source.max < target.min or target.max < source.min:
            target.min = target.max = 0
        elif source.min == source.max == target.min == target.max:
            target.min = target.max = 1
        else:
            target.min = 0
            target.max = 1
    elif i_type == InstructionType.MOD:
        if target.min == target.max and source.min == source.max:
            target.max = target.min = target.min % source.min
        elif target.max < source.min:
            # No change to target's values
            pass
        else:
            target.min = 0
            target.max = min(source.max - 1, target.max)
    elif i_type == InstructionType.MUL:
        new_max = int(target.max * source.max)
        new_min = int(target.min * source.min)
        neg_min = int(target.min * source.max)
        neg_max = int(target.max * source.min)
        target.max = max(new_max, new_min, neg_min, neg_max)
        target.min = min(new_min, new_max, neg_min, neg_max)

    if target.min > target.max:
        raise Unhandled


def load_code(path: str) -> List[Instruction]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    return [decode(line) for line in lines]


if __name__ == "__main__":
    def main():
        if len(argv) >= 2 and argv[1] == "--debug":
            debug_dump("input/d24.txt")
        elif len(argv) >= 2 and argv[1] == "--debug-redux":
            debug_dump("input/d24_reduced.txt")
        elif len(argv) >= 2 and argv[1] == "--attempt-reduction":
            program = load_code("input/d24.txt")
            upper_bounds = [1, 3, 3] + [9] * 11
            max_value = "".join([str(bound) for bound in reduce_bounds(program, upper_bounds)])
            print(f"Max value: {max_value}")
            lower_bounds = [1] * 14
            min_value = "".join([str(bound) for bound in reduce_bounds_from_below(program,
                                                                                  lower_bounds)])
            print(f"Min value: {min_value}")
        else:
            program = load_code("input/d24.txt")
            dependencies = track_dependencies(program)
            print(display_registers(dependencies))
    main()
