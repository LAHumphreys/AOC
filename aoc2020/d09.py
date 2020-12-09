from tools.file_loader import load_ints
from tools.list_ops import find_sum_pair, find_sum_range


def is_valid(check_slice, to_check):
    return find_sum_pair(check_slice, to_check)


def part_one(values, num_check_digits):
    i = num_check_digits
    invalid = None
    while i < len(values) and invalid is None:
        check_slice = values[i - num_check_digits:i]
        to_check = values[i]
        if is_valid(check_slice, to_check) is None:
            invalid = to_check
        i += 1
    return invalid


def part_two(values, invalid_target):
    [start_index, end_index] = find_sum_range(values, invalid_target)
    invalid_range = values[start_index:end_index + 1]
    result = min(invalid_range) + max(invalid_range)
    return result


if __name__ == "__main__":
    def main():
        values = load_ints("input/d09.txt")
        invalid_number = part_one(values, 25)
        print(invalid_number)
        print(part_two(values, invalid_number))
    main()
