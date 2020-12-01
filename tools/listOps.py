import copy

def NonSortedMatchGroups(A, B, key=None):
    """
    Return all sets of matching elements. Note that is different to
    NonSortedIntersection which returns a unique list of matching
    elements.

    STOP: If you simply want a list of matches, you may want
          NonSortedIntersection

    :param A:   A list to be compared to list B
    :param B:   A list to be compared to list A
    
    :param key: Optional transform of an item, used to sort and check equality

    :return: A list where each element representing a matching value. It is a set
             with two items:
                 0: A list of items from A which matched the item in [1]
                 1: A list of items from B which matched the item in [0]
             e.g [([1], [1,1]), ([2,2], [2,2])]
    """
    listA = copy.copy(A)
    listB = copy.copy(B)
    listA.sort(key=key)
    listB.sort(key=key)

    ia = 0
    ib = 0
    matches = []
    lenA = len(listA)
    lenB = len(listB)

    def lt(lhs, rhs):
        if key != None:
            return key(lhs) < key(rhs)
        else:
            return lhs < rhs

    def eq(lhs, rhs):
        if key != None:
            return key(lhs) == key(rhs)
        else:
            return lhs == rhs

    while ia < lenA and ib < lenB:
        a = listA[ia]
        b = listB[ib]

        doMatches = False

        if eq(a,b):
            doMatches = True
        elif lt(a,b):
            ia+=1
        else:
            ib+=1

        if doMatches:
            matchesA = []
            matchesB = []
            while ia < (lenA) and eq(listA[ia], a):
                matchesA.append(listA[ia])
                ia += 1

            while ib < (lenB) and eq(listB[ib], b):
                matchesB.append(listB[ib])
                ib += 1

            matches.append( (matchesA, matchesB))

    return matches


def NonSortedIntersection(A: list, B: list, key=None):
    """
    Look for items that appear in both lists A and B.

    This varient returns a single list of unique matches. If there are duplicate
    matches, no guarentee is made as to which of the duplicates are returned.

    :param A:   A list to be compared to list B
    :param B:   A list to be compared to list A

    :param key: Optional transform of an item, used to sort and check equality

    :return: A list of unique items that appear in both lists A and B.
             The list is sorted in ascending order and any duplicates are
             removed.
    """

    listA = copy.copy(A)
    listB = copy.copy(B)
    listA.sort(key=key)
    listB.sort(key=key)
    ia = 0
    ib = 0
    matches = []
    lenA = len(listA)
    lenB = len(listB)

    def lt(lhs, rhs):
        if key !=None:
            return key(lhs) < key(rhs)
        else:
            return lhs < rhs

    def eq(lhs, rhs):
        if key != None:
            return key(lhs) == key(rhs)
        else:
            return lhs == rhs

    while ia < lenA and ib < lenB:
        a = listA[ia]
        b = listB[ib]
        while ia < (lenA-1) and eq(listA[ia+1], a):
            ia+=1
        while ib < (lenB -1) and eq(listB[ib+1], b):
            ib+=1

        if eq(a,b):
            matches.append(a)
            ia+=1
            ib+=1
        elif lt(a,b):
            ia+=1
        else:
            ib+=1

    return matches

class ListTooShort(Exception):
    pass

def FindSumPairPreSorted(numbers: list, target: int):
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
    listLen = len(numbers)
    if (listLen < 2):
        raise ListTooShort

    found = False
    baseLow = 0
    high = 1
    while not found and baseLow < (listLen -1):
        low = baseLow

        while high > (low+1) and (numbers[low] + numbers[high]) > target:
            high -= 1

        while high < (listLen-1) and (numbers[low] + numbers[high]) < target:
            high += 1

        if (numbers[low] + numbers[high]) == target:
            found = True
        else:
            baseLow += 1

    if found:
        return [numbers[low], numbers[high]]
    else:
        return None

def FindSumPair(numbers: list, target: int):
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
    sortedNumbers = copy.copy(numbers)
    sortedNumbers.sort()
    return FindSumPairPreSorted(sortedNumbers, target)



def FindSumTrio(unSortedNumbers: list, target: int):
    """
    Search the sorted list of numbers for a triplet of numbers who's
    value sum to target.

    The function accepts an unosrted list of numbers. The operation is
    non-destructive since a shallow copy of numbers is taken before it is
    sorted

    :param numbers: Numbers to be searched
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
    numbers = copy.copy(unSortedNumbers)
    numbers.sort()

    listLen = len(numbers)
    if (listLen < 3):
        raise ListTooShort

    low = 0
    result = None
    while result is None and low < (listLen -2):
        pairs = numbers[low+1:]
        targetPairSum = target - numbers[low]
        pair = FindSumPairPreSorted(pairs,targetPairSum)

        if pair is not None:
            result = [numbers[low], pair[0], pair[1]]
        else:
            low += 1

    return result

