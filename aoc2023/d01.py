def load_calibration(file_name) -> list[str]:
    with open(file_name, "r", encoding='utf-8') as input_file:
        return [ln.replace("\n", "") for ln in input_file.readlines()]


def calculate_calibration(lines: list[str]) -> int:
    calibration = 0
    for ln in lines:
        numerics = [c for c in ln if '0' <= c <= '9']
        calibration += int(numerics[0] + numerics[-1])

    return calibration


def calculate_calibration2(lines: list[str]) -> int:
    return sum(find_numeric(ln) for ln in lines)


def find_numeric(ln: str) -> int:
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    min_number_size = min(len(n) for n in numbers)
    max_number_size = max(len(n) for n in numbers)
    number_map = {numbers[i]: i for i in range(len(numbers))}
    digits = {str(i): i for i in range(10)}
    first = None
    last = None
    i = 0
    while not first and i < len(ln):
        if ln[i] in digits:
            first = digits[ln[i]]
        slice_size = min_number_size
        while not first and (i+slice_size) <= len(ln):
            token = ln[i:i+slice_size]
            if token in number_map:
                first = number_map[token]
            slice_size += 1
        i += 1

    i = len(ln) - 1
    while not last and i >= 0:
        if ln[i] in digits:
            last = digits[ln[i]]
        slice_size = min_number_size
        while not last and (i-slice_size) >= 0 and slice_size <= max_number_size:
            token = ln[i - slice_size + 1:i+1]
            if token in number_map:
                last = number_map[token]
            slice_size += 1
        i -= 1
    print(str(first) + str(last))
    return int(str(first) + str(last))


def main():
    lines = load_calibration("input/d01.txt")
    print(calculate_calibration(lines))
    print(calculate_calibration2(lines))


if __name__ == "__main__":
    main()
