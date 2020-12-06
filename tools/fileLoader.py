import re

from tools.dictTools import build_dicts


def load_ints(file):
    result = []
    with open(file) as f:
        for lin in f.readlines():
            result.append(int(lin))

    return result


def load_int_list(file):
    result = []
    with open(file) as f:
        for tok in f.read().split(","):
            result.append(int(tok))

    return result


def load_lists(file):
    result = []
    with open(file) as f:
        for lin in f.readlines():
            if lin[-1] == "\n":
                lin = lin[0:-1]
            working = []
            for tok in lin.split(","):
                working.append(tok)
            result.append(working)

    return result


def load_string_groups(file):
    result = []
    with open(file) as f:
        thisGroup = []
        for lin in f.readlines():
            if lin[-1] == "\n":
                lin = lin[0:-1]
            if len(lin) == 0:
                if len(thisGroup) > 0:
                    result.append(thisGroup)
                    thisGroup = []
            else:
                thisGroup.append(lin)
        if len(thisGroup) > 0:
            result.append(thisGroup)
    return result


class UnexpectedLineFormat(Exception):
    pass


class UnexpectedNumberOfRows(Exception):
    pass


def load_patterns(parser_regex, file, numResults=None):
    result = []
    with open(file) as f:
        for lin in f.readlines():
            m = parser_regex.search(lin)
            if m is not None:
                result.append(m.groups())
            else:
                raise UnexpectedLineFormat
    if numResults is not None:
        if numResults != len(result):
            raise UnexpectedNumberOfRows

    return result


anyRegex = re.compile(".*")


def load_one(file, validator=anyRegex):
    result = None
    with open(file) as f:
        lines = f.readlines()
        if len(lines) != 1:
            raise UnexpectedNumberOfRows
        result = lines[0]
        if result[-1] == "\n":
            result = result[:-1]
        if not validator.match(result):
            raise UnexpectedLineFormat
    return result


def load_dicts(file):
    with (open(file)) as f:
        lines = f.read()
        result = build_dicts(lines)

    return result
