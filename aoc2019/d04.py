from tools.combinations import generate_ascending


def valid_value(val, req_run=None):
    valid = False
    got_required = False

    if req_run is None:
        got_required = True

    if len(val) == 6:
        last = val[0]
        run = 1
        longest_run = 1
        for value in val[1:]:
            if value == last:
                run += 1
            elif value < last:
                return False
            else:
                if run > longest_run:
                    longest_run = run
                if run == req_run:
                    got_required = True
                run = 1
            last = value

        if run > longest_run:
            longest_run = run

        if run == req_run:
            got_required = True

        if longest_run >= 2 and got_required:
            valid = True

    return valid


def valid_value_2(val):
    return valid_value(val, req_run=2)


if __name__ == "__main__":
    MIN_VALUE = [1, 5, 3, 5, 1, 7]
    MAX_VALUE = [6, 3, 0, 3, 9, 5]


    def main():
        num_part_1 = 0
        num_part_2 = 0
        for generated in generate_ascending(
                6, [1, 2, 3, 4, 5, 6, 7, 8, 9],
                min_value=MIN_VALUE, max_value=MAX_VALUE):
            if valid_value(generated):
                num_part_1 += 1

            if valid_value_2(generated):
                num_part_2 += 1

        print("Part 1: {0}".format(num_part_1))
        print("Part 2: {0}".format(num_part_2))


    main()
