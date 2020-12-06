import re

from tools.file_loader import load_patterns
from tools.string_operations import count_chars

SPLIT_REGEX = re.compile("^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$")


def is_pass_valid(split_groups):
    char = split_groups[2]
    lower = int(split_groups[0])
    upper = int(split_groups[1])
    passwd = split_groups[3]

    valid = True
    count = {}
    count_chars(passwd, count)
    if char not in count:
        valid = False
    elif count[char] < lower:
        valid = False
    elif count[char] > upper:
        valid = False

    return valid


def is_pass_valid_part_2(split_groups):
    char = split_groups[2]
    lower = int(split_groups[0]) - 1
    upper = int(split_groups[1]) - 1
    passwd = split_groups[3]

    valid = True
    if upper >= len(passwd):
        valid = False
    else:
        has_lower = (passwd[lower] == char)
        has_upper = (passwd[upper] == char)
        if has_lower and has_upper:
            valid = False
        elif not has_lower and not has_upper:
            valid = False

    return valid


if __name__ == "__main__":
    def main():
        passes = load_patterns(SPLIT_REGEX, "input/d02.txt")
        count = 0
        count2 = 0
        for pass_to_test in passes:
            if is_pass_valid(pass_to_test):
                count += 1
            if is_pass_valid_part_2(pass_to_test):
                count2 += 1
        print("Valid: {0}".format(count))
        print("Valid (2): {0}".format(count2))

    main()
