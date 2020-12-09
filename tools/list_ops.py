"""
Utilities and algorithms for manipulating list like structures
"""
import copy


def make_lt(key):
    """
    Internal tools less-than comparator factory function
    """
    if key is not None:
        def less_than(lhs, rhs):
            return key(lhs) < key(rhs)
    else:
        def less_than(lhs, rhs):
            return lhs < rhs
    return less_than


def make_eq(key):
    """
    Internal tools equals comparator factory function
    """
    if key is not None:
        def equals(lhs, rhs):
            return key(lhs) == key(rhs)
    else:
        def equals(lhs, rhs):
            return lhs == rhs
    return equals


def count_items_across_groups(groups):
    """
    Given a list of iterables, returns the number of times each
    unique item appears across all of the lists.

    :param groups: A group of lists, each of which should be iterated over

    :return: A dict mapping from item to the count of occurrences
    """
    result = {}
    for group in groups:
        for item in group:
            if item not in result:
                result[item] = 1
            else:
                result[item] += 1
    return result


def unsorted_matched_groups(list_a, list_b, key=None):
    """
    Return all sets of matching elements. Note that is different to
    NonSortedIntersection which returns a unique list of matching
    elements.

    STOP: If you simply want a list of matches, you may want
          NonSortedIntersection

    :param list_a:   A list to be compared to list B
    :param list_b:   A list to be compared to list A

    :param key: Optional transform of an item, used to sort and check equality

    :return: A list where each element representing a matching value. It is a set
             with two items:
                 0: A list of items from A which matched the item in [1]
                 1: A list of items from B which matched the item in [0]
             e.g [([1], [1,1]), ([2,2], [2,2])]
    """
    list_a = copy.copy(list_a)
    list_b = copy.copy(list_b)
    list_a.sort(key=key)
    list_b.sort(key=key)

    matches = []
    len_a = len(list_a)
    len_b = len(list_b)

    less_than = make_lt(key)
    equals = make_eq(key)

    index_a = index_b = 0
    while index_a < len_a and index_b < len_b:
        item_a = list_a[index_a]
        item_b = list_b[index_b]

        do_matches = False

        if equals(item_a, item_b):
            do_matches = True
        elif less_than(item_a, item_b):
            index_a += 1
        else:
            index_b += 1

        if do_matches:
            matches_a = []
            matches_b = []
            while index_a < len_a and equals(list_a[index_a], item_a):
                matches_a.append(list_a[index_a])
                index_a += 1

            while index_b < len_b and equals(list_b[index_b], item_b):
                matches_b.append(list_b[index_b])
                index_b += 1

            matches.append((matches_a, matches_b))

    return matches


def non_sorted_intersection(list_a: list, list_b: list, key=None):
    """
    Look for items that appear in both lists A and B.

    This variant returns a single list of unique matches. If there are duplicate
    matches, no guarantee is made as to which of the duplicates are returned.

    :param list_a:   A list to be compared to list B
    :param list_b:   A list to be compared to list A

    :param key: Optional transform of an item, used to sort and check equality

    :return: A list of unique items that appear in both lists A and B.
             The list is sorted in ascending order and any duplicates are
             removed.
    """

    list_a = copy.copy(list_a)
    list_b = copy.copy(list_b)
    list_a.sort(key=key)
    list_b.sort(key=key)
    index_a = 0
    index_b = 0
    matches = []
    len_a = len(list_a)
    len_b = len(list_b)

    less_than = make_lt(key)
    equals = make_eq(key)

    while index_a < len_a and index_b < len_b:
        item_a = list_a[index_a]
        item_b = list_b[index_b]
        while index_a < (len_a - 1) and equals(list_a[index_a + 1], item_a):
            index_a += 1
        while index_b < (len_b - 1) and equals(list_b[index_b + 1], item_b):
            index_b += 1

        if equals(item_a, item_b):
            matches.append(item_a)
            index_a += 1
            index_b += 1
        elif less_than(item_a, item_b):
            index_a += 1
        else:
            index_b += 1

    return matches


class BadDimensions(Exception):
    """
    Thrown if the specified number dimensions does not match the data provided
    """


def split_to_dims(iterable, dimensions: tuple):
    """
    Assemble a multidimensional list by iterating over iterable
    and placing the items into lists of lengths specified by
    dimensions.

    e.g split_split_to_dims("1234", (2,2)) => [["1", "2"], ["3", "4"]]

    If desired the final dimension may be left as None to indicate
    as many copies as can be fulfilled by the input

    e.g split_split_to_dims("123456", (2,None))
            => [["1", "2"], ["3", "4"], ["5", "6"]]

    :param iterable: The item generator
    :param dimensions: A tuple of integer dimensions. The first item in the tuple
                       is the inner most dimension.
                       The final item may be None, to indicate "any" length

    :return: A list of lists (of lists..), with lengths specified by dimensions
    """
    stacking = False
    result = None
    if dimensions[-1] is None:
        stacking = True
        dimensions = dimensions[:-1]
        result = []

    number_of_dimensions = len(dimensions)
    stack = [[] for _ in range(number_of_dimensions)]
    for item in iterable:
        stack[0].append(item)
        i = 0
        while i < (number_of_dimensions - 1) and len(stack[i]) == dimensions[i]:
            stack[i + 1].append(copy.copy(stack[i]))
            stack[i] = []
            i += 1
        if len(stack[-1]) == dimensions[-1]:
            if stacking:
                result.append(copy.copy(stack[-1]))
            elif result is not None:
                raise BadDimensions
            else:
                result = copy.copy(stack[-1])
            stack[-1] = []

    if result is None:
        raise BadDimensions

    for dim in stack:
        if len(dim) != 0:
            raise BadDimensions

    return result


def find_sum_range(values: list, target):
    """
    Search the provided list of values for a contiguous range
    of values that sum to the provided target. If not primitives,
    the list objects must implement the following methods:
          __add__,
          __eq__,
          __lt__
    :param values:       A list of values to search
    :param target:       The value the range must sum to
    :return:             [start index, end index] of the range, or None
                         if there is no such range
    """
    num_values = len(values)

    start_index = 0
    result = None
    while result is None and start_index < num_values:
        range_sum = values[start_index]
        end_index = start_index

        while range_sum != target and end_index < (num_values - 1):
            end_index += 1
            range_sum += values[end_index]

        if range_sum == target:
            result = (start_index, end_index)
        start_index += 1

    return result


class ListTooShort(Exception):
    """
    Raised if insufficient items have been provided to perform the requested operation
    """


def find_sum_pair_presorted(numbers: list, target: int):
    """
    Search the sorted list of numbers for a pair of numbers who's
    value sum to target.

    Providing a non-sorted list will result in undefined behaviour.

    :param numbers: Numbers to be searched, already sorted in ascending order
    :param target:  The value the pair of numbers must sum to

    :return: The pair of numbers [a, b] which are distinct members of numbers,
             and which satisfy the conditions:
                 a + b = target
                 a <= b

             If no such pair exists, None is returned

             If multiple such pairs exist the pair with the lowest value of a
             is returned
    """
    list_len = len(numbers)
    if list_len < 2:
        raise ListTooShort

    found = False
    base_low = 0
    high = 1
    while not found and base_low < (list_len - 1):
        low = base_low

        while high > (low + 1) and (numbers[low] + numbers[high]) > target:
            high -= 1

        while high < (list_len - 1) and (numbers[low] + numbers[high]) < target:
            high += 1

        if (numbers[low] + numbers[high]) == target:
            found = True
        else:
            base_low += 1

    result = None
    if found:
        result = [numbers[base_low], numbers[high]]

    return result


def find_sum_pair(numbers: list, target: int):
    """
    Wrapper around FindSumPairSorted that handles non-sorted input

    Operation is non-destructive as a shallow copy is taken prior to sorting
    the input

    :param numbers: Numbers to be searched
    :param target:  The value the pair of numbers must sum to

    :return: The pair of numbers [a, b] which are distinct members of numbers,
             and which satisfy the conditions:
                 a + b = target
                 a <= b

             If no such pair exists, None is returned

             If multiple such pairs exist the pair with the lowest value of a
             is returned
    """
    sorted_numbers = sorted(copy.copy(numbers))
    return find_sum_pair_presorted(sorted_numbers, target)


def find_sum_trio(unsorted_numbers: list, target: int):
    """
    Search the sorted list of numbers for a triplet of numbers who's
    value sum to target.

    The function accepts an unsorted list of numbers. The operation is
    non-destructive since a shallow copy of numbers is taken before it is
    sorted

    :param unsorted_numbers: Numbers to be searched
    :param target:  The value the trio of numbers must sum to

    :return: A trio of numbers [a, b, c] which are distinct members of numbers,
             and which satisfy the conditions:
                 a + b + c= target
                 a <= b <= c

             If no such trio exists, None is returned

             If multiple such trios exist the trio with the lowest value of a
             is returned. And if multiple exist for that value of a, the trio
             with the lowest value of b is returned
    """
    numbers = sorted(copy.copy(unsorted_numbers))

    list_len = len(numbers)
    if list_len < 3:
        raise ListTooShort

    low = 0
    result = None
    while result is None and low < (list_len - 2):
        pairs = numbers[low + 1:]
        target_pair_sum = target - numbers[low]
        pair = find_sum_pair_presorted(pairs, target_pair_sum)

        if pair is not None:
            result = [numbers[low], pair[0], pair[1]]
        else:
            low += 1

    return result
