import copy

from tools.file_loader import load_ints
from tools.list_ops import find_sum_pair


def is_valid(check_slice, to_check):
    check_digits = copy.copy(check_slice)
    check_digits.sort()
    return find_sum_pair(check_digits, to_check)


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
    start_index = 0
    result = None
    while result is None and start_index < len(values):
        range_sum = 0
        end_index = start_index
        while end_index < len(values) and range_sum < invalid_target:
            range_sum += values[end_index]
            if range_sum == invalid_target:
                invalid_range = values[start_index:end_index+1]
                invalid_range.sort()
                result = invalid_range[0] + invalid_range[-1]
            end_index += 1
        start_index += 1
    return result


if __name__ == "__main__":
    def main():
        values = load_ints("input/d09.txt")
        invalid_number = part_one(values, 25)
        print(invalid_number)
        print(part_two(values, invalid_number))
    main()
