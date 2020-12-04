import re
from tools.fileLoader import LoadPatterns
from tools.stringsOps import countChars
splitRegex = re.compile("^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$")

def isPassValid(splitGroups):
    char = splitGroups[2]
    lower = int(splitGroups[0])
    upper = int(splitGroups[1])
    passwd = splitGroups[3]

    valid = True
    count = {}
    countChars(passwd, count)
    if char not in count:
        valid = False
    elif count[char] < lower:
        valid = False
    elif count[char] > upper:
        valid = False

    return valid

def isPassValid2(splitGroups):
    char = splitGroups[2]
    lower = int(splitGroups[0])-1
    upper = int(splitGroups[1])-1
    passwd = splitGroups[3]

    valid = True
    if upper >= len(passwd):
        valid = False
    else:
        hasLower = (passwd[lower] == char)
        hasUpper = (passwd[upper] == char)
        if hasLower and hasUpper:
            valid = False
        elif not hasLower and not hasUpper:
            valid = False

    return valid


if __name__ == "__main__":
    passes = LoadPatterns(splitRegex, "input/d02.txt")
    count = 0
    count2 = 0
    for p in passes:
        if isPassValid(p):
            count += 1
        if isPassValid2(p):
            count2 += 1
    print ("Valid: {0}".format(count))
    print ("Valid (2): {0}".format(count2))
