import copy


def make_lt(key):
    if key is not None:
        return lambda lhs, rhs: key(lhs) < key(rhs)
    else:
        return lambda lhs, rhs: lhs < rhs


def make_eq(key):
    if key is not None:
        return lambda lhs, rhs: key(lhs) == key(rhs)
    else:
        return lambda lhs, rhs: lhs == rhs


def unsorted_matched_groups(a, b, key=None):
    """
    Return all sets of matching elements. Note that is different to
    NonSortedIntersection which returns a unique list of matching
    elements.

    STOP: If you simply want a list of matches, you may want
          NonSortedIntersection

    :param a:   A list to be compared to list B
    :param b:   A list to be compared to list A

    :param key: Optional transform of an item, used to sort and check equality

    :return: A list where each element representing a matching value. It is a set
             with two items:
                 0: A list of items from A which matched the item in [1]
                 1: A list of items from B which matched the item in [0]
             e.g [([1], [1,1]), ([2,2], [2,2])]
    """
    list_a = copy.copy(a)
    list_b = copy.copy(b)
    list_a.sort(key=key)
    list_b.sort(key=key)

    matches = []
    len_a = len(list_a)
    len_b = len(list_b)

    lt = make_lt(key)
    eq = make_eq(key)

    ia = ib = 0
    while ia < len_a and ib < len_b:
        a = list_a[ia]
        b = list_b[ib]

        do_matches = False

        if eq(a, b):
            do_matches = True
        elif lt(a, b):
            ia += 1
        else:
            ib += 1

        if do_matches:
            matches_a = []
            matches_b = []
            while ia < len_a and eq(list_a[ia], a):
                matches_a.append(list_a[ia])
                ia += 1

            while ib < len_b and eq(list_b[ib], b):
                matches_b.append(list_b[ib])
                ib += 1

            matches.append((matches_a, matches_b))

    return matches


def non_sorted_intersection(a: list, b: list, key=None):
    """
    Look for items that appear in both lists A and B.

    This variant returns a single list of unique matches. If there are duplicate
    matches, no guarantee is made as to which of the duplicates are returned.

    :param a:   A list to be compared to list B
    :param b:   A list to be compared to list A

    :param key: Optional transform of an item, used to sort and check equality

    :return: A list of unique items that appear in both lists A and B.
             The list is sorted in ascending order and any duplicates are
             removed.
    """

    list_a = copy.copy(a)
    list_b = copy.copy(b)
    list_a.sort(key=key)
    list_b.sort(key=key)
    ia = 0
    ib = 0
    matches = []
    len_a = len(list_a)
    len_b = len(list_b)

    lt = make_lt(key)
    eq = make_eq(key)

    while ia < len_a and ib < len_b:
        a = list_a[ia]
        b = list_b[ib]
        while ia < (len_a - 1) and eq(list_a[ia + 1], a):
            ia += 1
        while ib < (len_b - 1) and eq(list_b[ib + 1], b):
            ib += 1

        if eq(a, b):
            matches.append(a)
            ia += 1
            ib += 1
        elif lt(a, b):
            ia += 1
        else:
            ib += 1

    return matches


class ListTooShort(Exception):
    pass


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

    if found:
        return [numbers[base_low], numbers[high]]
    else:
        return None


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
