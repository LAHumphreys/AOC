from dataclasses import dataclass


@dataclass
class PartNumber:
    start_idx: int
    end_idx: int
    value: int


@dataclass
class Gear:
    x: int
    y: int


@dataclass
class BluePrint:
    max_x: int
    max_row: int
    row_maps: [list[list[bool]]]
    part_numbers: [list[list[PartNumber]]]
    gears: list[Gear]


def is_valid_part(start_idx: int, stop_idx: int, row: int, blue_print: BluePrint) -> bool:
    row_map = blue_print.row_maps[row]
    row_map_after = blue_print.row_maps[min(row+1, blue_print.max_row)]
    row_map_before = blue_print.row_maps[max(row-1, 0)]
    consolidated_row_map = [x for x in map(any, zip(row_map, row_map_after, row_map_before))]
    return any(map(lambda i: consolidated_row_map[i], range(start_idx, stop_idx+1)))


def is_digit(symbol: str) -> bool:
    if len(symbol) != 1:
        raise ValueError
    return "0" <= symbol <= "9"


def is_symbol(symbol: str) -> bool:
    if len(symbol) != 1:
        raise ValueError
    return not (is_digit(symbol) or symbol == ".")


def map_row(line: str) -> list[bool]:
    symbols = [is_symbol(token) for token in line]
    prior = [False] + symbols
    after = symbols[1:] + [False]
    return [valid for valid in map(any, zip(prior, symbols, after))]


@dataclass
class Token:
    value: str
    start_idx: int
    stop_idx: int


def get_parts(line: str) -> list[PartNumber]:
    tokens = (Token(value=tok[1],
                    start_idx=tok[0],
                    stop_idx=tok[0]) for tok in enumerate(line) if is_digit(tok[1]))

    grouped_tokens = []
    for token in tokens:
        if grouped_tokens and grouped_tokens[-1].stop_idx == (token.stop_idx-1):
            grouped_tokens[-1].stop_idx += 1
            grouped_tokens[-1].value += token.value
        else:
            grouped_tokens.append(token)

    return [PartNumber(start_idx=tok.start_idx,
                       end_idx=tok.stop_idx,
                       value=int(tok.value)) for tok in grouped_tokens]


def get_gears(lines: list[str]) -> list[Gear]:
    gears = []
    for y, line in enumerate(lines):
        gears += [Gear(x=x, y=y) for x, token in enumerate(line) if token == "*"]
    return gears


def get_ratios(blue_print: BluePrint, gear: Gear) -> list[int]:
    parts = blue_print.part_numbers[gear.y]
    if gear.y > 0:
        parts = blue_print.part_numbers[gear.y-1] + parts
    if gear.y < blue_print.max_row:
        parts += blue_print.part_numbers[gear.y+1]
    ratios = []
    for part in parts:
        if part.start_idx < gear.x and part.end_idx >= gear.x-1:
            ratios.append(part.value)
        elif gear.x <= part.start_idx <= gear.x+1:
            ratios.append(part.value)
    return ratios


def load_blue_print(file_name: str) -> BluePrint:
    with open(file_name) as input_file:
        lines = [line.replace("\n", "") for line in input_file.readlines()]
        return BluePrint(
            max_x=len(lines[0]) - 1,
            max_row=len(lines) - 1,
            row_maps=[map_row(line) for line in lines],
            part_numbers=[get_parts(line) for line in lines],
            gears=get_gears(lines))


def part_check_1(row_idx: 2, part: PartNumber, blue_print: BluePrint) -> bool:
    return is_valid_part(part.start_idx, part.end_idx, row_idx, blue_print)


def part_one(blue_print: BluePrint) -> int:
    total = 0
    for row_idx, row in enumerate(blue_print.part_numbers):
        total += sum(part.value for part in row if part_check_1(row_idx, part, blue_print))
    return total


def part_two(blue_print: BluePrint) -> int:
    ratios = map(lambda gear: get_ratios(blue_print, gear), blue_print.gears)
    product = 0
    for ratio in ratios:
        if len(ratio) == 2:
            product += ratio[0]*ratio[1]
    return product


def main():
    blue_print = load_blue_print("input/d03.txt")
    print(part_one(blue_print))
    print(part_two(blue_print))
    pass


if __name__ == "__main__":
    main()
