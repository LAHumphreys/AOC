from tools.file_loader import load_one, load_ints


class BadDiff(Exception):
    pass


class BadDim(Exception):
    pass


def load_adapters(path):
    adapters = load_ints(path)
    adapters.append(0)
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    return adapters


def part_1(path):
    adapters = load_adapters(path)
    unit_diffs = 0
    triple_unit_diffs = 0
    i = 1
    while i < len(adapters):
        diff = adapters[i] - adapters[i-1]
        if diff == 1:
            unit_diffs += 1
        elif diff == 3:
            triple_unit_diffs += 1
        else:
            raise BadDiff
        i += 1
    return triple_unit_diffs * unit_diffs


class UnhandledCase(Exception):
    pass


def part_2(path):
    adapters = load_adapters(path)
    num_adapters = len(adapters)
    combinations = 1
    fix_index = 1
    free_length = 0
    last_jolt = adapters[0]
    while fix_index < (num_adapters-1):
        this_jolt = adapters[fix_index]
        next_jolt = adapters[fix_index+1]
        if this_jolt - last_jolt == 1 and next_jolt - this_jolt == 1:
            free_length += 1
        else:
            if free_length < 1:
                pass
            elif free_length == 1:
                combinations *= 2
            elif free_length == 2:
                combinations *= 4
            elif free_length == 3:
                combinations *= 7
            else:
                raise UnhandledCase
            free_length = 0
        fix_index +=1
        last_jolt = this_jolt
    return combinations


if __name__ == "__main__":
    def main():
        print(part_1("input/d10.txt"))
        print(part_2("input/d10.txt"))
    main()