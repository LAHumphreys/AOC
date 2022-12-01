"""
Common text file parsing for AOC style problems
"""
import re

from .dictionary_tools import build_dicts


def load_ints(file):
    """
    Attempt to interpret each line of a text file as an integer
    """
    result = []
    with open(file, encoding="ascii") as file_handle:
        for lin in file_handle.readlines():
            result.append(int(lin))

    return result


def load_int_list(file):
    """
    Attempt to interpret each line of a text file as comma separated list of integers
    """
    result = []
    with open(file, encoding="ascii") as file_handle:
        for tok in file_handle.read().split(","):
            result.append(int(tok))

    return result


def load_lists(file):
    """
    Attempt to interpret each line of a text file as comma separated list of strings
    """
    result = []
    with open(file, encoding="ascii") as file_handle:
        for lin in file_handle.readlines():
            if lin[-1] == "\n":
                lin = lin[0:-1]
            working = []
            for tok in lin.split(","):
                working.append(tok)
            result.append(working)

    return result


def load_int_groups(file: str) -> list[list[int]]:
    """
    Split a file into sets of ints (separated by a blank line)
    The result is a list of lists. Where each inner list is the
    list of the ints on each line. E.g:
        1
        2
        3

        3
        4

        6
        => [[1, 2 ,3], [3, 4], [6]]
    """
    string_groups = load_string_groups(file)
    result = []
    for group in string_groups:
        result.append([int(x) for x in group])
    return result

def load_string_groups(file):
    """
    Split a file into paragraphs (separated by a blank line)
    The result is a list of lists. Where each inner list is the
    list of lines (string) in that paragraph
    """
    result = []
    with open(file, encoding="ascii") as file_handle:
        this_group = []
        for lin in file_handle.readlines():
            if lin[-1] == "\n":
                lin = lin[0:-1]
            if len(lin) == 0:
                if len(this_group) > 0:
                    result.append(this_group)
                    this_group = []
            else:
                this_group.append(lin)
        if len(this_group) > 0:
            result.append(this_group)
    return result


class UnexpectedLineFormat(Exception):
    """
    Thrown when a parsing expression cannot handle an input line
    """


class UnexpectedNumberOfRows(Exception):
    """
    Thrown when the number of lines in an input file does not match the specified expected count
    """


def load_patterns(parser_regex, file, num_results=None):
    """
    Load a file in, returning a list where each item represents a line
    in the file. Instead of returning the raw string, instead return
    the list of matched groups from the provided regex
    """
    result = []
    with open(file, encoding="ascii") as file_handle:
        for lin in file_handle.readlines():
            match = parser_regex.search(lin)
            if match is not None:
                result.append(match.groups())
            else:
                raise UnexpectedLineFormat
    if num_results is not None:
        if num_results != len(result):
            raise UnexpectedNumberOfRows

    return result


MATCH_ANY = re.compile(".*")


def load_one(file, validator=MATCH_ANY):
    """
    Load a one line text file, optionally applying a regex as validation
    of expected format
    """
    result = None
    with open(file, encoding="ascii") as file_handle:
        lines = file_handle.readlines()
        if len(lines) != 1:
            raise UnexpectedNumberOfRows
        result = lines[0]
        if result[-1] == "\n":
            result = result[:-1]
        if not validator.match(result):
            raise UnexpectedLineFormat
    return result


def load_dicts(file):
    """
    Load a text file where each paragraph (separated by a blank line)
    is interpreted as a set of key value pairs.

    e.g
       k1:v1 k2:v2
       k3:v3

       j1:w1 j2:w2
       ...
    """
    with (open(file, encoding="ascii")) as file_handle:
        lines = file_handle.read()
        result = build_dicts(lines)

    return result
