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
        for v in val[1:]:
            if v == last:
                run += 1
            elif v < last:
                return False
            else:
                if run > longest_run:
                    longest_run = run
                if run == req_run:
                    got_required = True
                run = 1
            last = v

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
    minValue = [1, 5, 3, 5, 1, 7]
    maxValue = [6, 3, 0, 3, 9, 5]
    numPart1 = 0
    numPart2 = 0
    for g in generate_ascending(
            6, [1, 2, 3, 4, 5, 6, 7, 8, 9],
            min_value=minValue, max_value=maxValue):
        if valid_value(g):
            numPart1 += 1

        if valid_value_2(g):
            numPart2 += 1

    print("Part 1: {0}".format(numPart1))
    print("Part 2: {0}".format(numPart2))
