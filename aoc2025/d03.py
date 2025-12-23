def load_sample(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def max_joltage_from_bank(bank: str) -> int:
    index, first = max(enumerate(bank[:-1]), key=lambda x: x[1])
    second = max(bank[index+1:])
    return int(first + second)

def unsafe_joltage_from_bank(bank: str) -> int:
    bank_len = len(bank)
    digits_remaining = 12
    first_idx = 0
    joltage_string = ""
    while digits_remaining > 0:
        digits_remaining -= 1
        index, next_digit = max(enumerate(bank[first_idx:bank_len-digits_remaining]), key=lambda x: x[1])
        joltage_string += next_digit
        first_idx += index + 1
    return int(joltage_string)

def part1(data: list[str]) -> int:
    return sum(max_joltage_from_bank(bank) for bank in data)


def part2(data: list[str]) -> int:
    return sum(unsafe_joltage_from_bank(bank) for bank in data)


def main():
    try:
        data = load_sample("input/d03.txt")
        print(f"Part 1: {part1(data)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
