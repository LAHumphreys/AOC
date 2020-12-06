"""
Utilities for generating combinations / permutations
"""
import itertools


class MinValueMismatch(Exception):
    """
    Thrown when the provided minimum value is not itself valie
    """


class MaxValueMismatch(Exception):
    """
    Thrown when the provided maximum value is not itself valie
    """


class MaxValueMisCalculation(Exception):
    """
    Thrown when the max value invalidates the provided initialisation params
    """


def extend_ascending(initial_value, e_valid_values, e_results):
    """
    Internal helper that takes an initial list value and appends
    all valid 1 item extensions to that list given a set of valid
    items
    """
    e_min_value = initial_value[-1]
    for value in e_valid_values:
        if value >= e_min_value:
            e_results.append(initial_value + [value])


def item_wise_less_than_or_equal(lhs, rhs):
    """
    Internal utility to check if lhs <= rhs
    """
    less_than = True
    i = 0
    while i < len(lhs) and less_than:
        less_than = lhs[i] <= rhs[i]
        i += 1
    return less_than


def extend_set_ascending(initial_values, valid_values,
                         min_value=None, max_value=None):
    """
    (recursive)

    Internal utility - not to be called directly
    """
    results = []
    init_is_min = False
    min_valid_values = []
    max_valid_values = []
    num_init_digits = len(initial_values[0])
    max_ind = -1

    if min_value is not None:
        init_is_min = True
        min_valid_values = filter(lambda item: item >= min_value[num_init_digits], valid_values)

    if max_value is not None:
        max_ind = 0
        max_valid_values = filter(lambda item: item <= max_value[num_init_digits], valid_values)

    for init in initial_values:
        init_is_min = init_is_min and item_wise_less_than_or_equal(init, min_value)

        while max_value is not None and \
                max_ind < num_init_digits and \
                init[max_ind] == max_value[max_ind]:

            if init[max_ind] > max_value[max_ind]:
                raise MaxValueMisCalculation
            max_ind += 1

        if init_is_min and max_ind == num_init_digits:
            min_max_valid_values = \
                filter(lambda item: item >= min_value[num_init_digits], max_valid_values)
            extend_ascending(init, min_max_valid_values, results)
        elif init_is_min:
            extend_ascending(init, min_valid_values, results)
        elif max_ind == num_init_digits:
            extend_ascending(init, max_valid_values, results)
        else:
            extend_ascending(init, valid_values, results)

    return results


def generate_ascending(length: int, valid_values: list,
                       min_value=None, max_value=None):
    """
    Dirty hacky variant of generate that imposes an additional
    constraint - the returned list must be in ascending order
    """
    if min_value is not None and len(min_value) != length:
        raise MinValueMismatch()

    if max_value is not None and len(max_value) != length:
        raise MaxValueMismatch()

    results = []
    if length > 0:
        for value in valid_values:
            if min_value is not None and min_value[0] > value:
                pass
            elif max_value is not None and max_value[0] < value:
                pass
            else:
                results.append([value])
        current_len = 1
        while current_len < length:
            current_len += 1
            results = extend_set_ascending(
                results, valid_values, min_value, max_value)
    return results


def generate(length: int, valid_values: list, consecutive_repeats=0):
    """
    Generate lists of fixed length from a set of valid values (which may repeat)

    An optional constraint may be imposed (consecutive_repeats) that requires
    at least one set of repeated digits.
    """
    results = []
    if length > 0:
        for value in valid_values:
            results.append([value])

        i = 1
        while i < length:
            new_results = []
            for header in results:
                for value in valid_values:
                    new_results.append(header + [value])
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


def generate_permutations(valid_values: list, choose: int):
    """
    Does what it says on the tine....
    """
    return list(itertools.permutations(valid_values, choose))
