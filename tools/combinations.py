import itertools


def extend_ascending(initial_value, valid_values, results):
    min_value = initial_value[-1]
    for v in valid_values:
        if v >= min_value:
            results.append(initial_value + [v])
    return results


class MinValueMismatch(Exception):
    pass


class MaxValueMismatch(Exception):
    pass


class MaxValueMisCalculation(Exception):
    pass


def extend_set_ascending(initial_values, valid_values,
                         min_value=None, max_value=None):
    results = []
    init_is_min = False
    min_valid_values = []
    max_valid_values = []
    num_init_digits = len(initial_values[0])
    max_ind = -1

    if min_value is not None:
        init_is_min = True
        for v in valid_values:
            if v >= min_value[num_init_digits]:
                min_valid_values.append(v)

    if max_value is not None:
        max_ind = 0
        for v in valid_values:
            if v <= max_value[num_init_digits]:
                max_valid_values.append(v)

    for init in initial_values:
        if init_is_min:
            for i in range(len(init)):
                if init[i] > min_value[i]:
                    init_is_min = False
                    break

        if max_value is not None:
            while max_ind < num_init_digits:
                if init[max_ind] > max_value[max_ind]:
                    raise MaxValueMisCalculation
                elif init[max_ind] == max_value[max_ind]:
                    max_ind += 1
                else:
                    break

        if init_is_min and max_ind == num_init_digits:
            min_max_valid_values = []
            for v in max_valid_values:
                if v >= min_value[num_init_digits]:
                    min_max_valid_values.append(v)
            extend_ascending(init, min_max_valid_values, results)
        elif init_is_min:
            extend_ascending(init, min_valid_values, results)
        elif max_ind == num_init_digits:
            extend_ascending(init, max_valid_values, results)
        else:
            extend_ascending(init, valid_values, results)
    return results


def generate_permutations(valid_values: list, choose: int):
    return [p for p in itertools.permutations(valid_values, choose)]


def generate_ascending(length: int, valid_values: list,
                       min_value=None, max_value=None):
    if min_value is not None and len(min_value) != length:
        raise MinValueMismatch()

    if max_value is not None and len(max_value) != length:
        raise MaxValueMismatch()

    results = []
    if length > 0:
        for v in valid_values:
            if min_value is not None and min_value[0] > v:
                pass
            elif max_value is not None and max_value[0] < v:
                pass
            else:
                results.append([v])
        current_len = 1
        while current_len < length:
            current_len += 1
            results = extend_set_ascending(
                results, valid_values, min_value, max_value)
    return results


def generate(length: int, valid_values: list, consecutive_repeats=0):
    results = []
    if length > 0:
        for v in valid_values:
            results.append([v])

        i = 1
        while i < length:
            new_results = []
            for header in results:
                for v in valid_values:
                    new_results.append(header + [v])
            results = new_results
            i += 1

        if consecutive_repeats > 0:
            new_results = []
            for result in results:
                repeated = 0
                i = 1
                while repeated < consecutive_repeats and i < length:
                    if result[i - 1 - repeated] == result[i]:
                        repeated += 1
                    else:
                        repeated = 0
                    i += 1
                if repeated >= consecutive_repeats:
                    new_results.append(result)

            results = new_results

    return results
