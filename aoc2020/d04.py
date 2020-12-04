from tools.fileLoader import LoadDicts
import re

class UnknownKey(Exception):
    pass


byrPattern = re.compile("^[1-2][0-9][0-9][0-9]$")
iyrPattern = re.compile("^2[0-9][0-9][0-9]$")
eyrPattern = re.compile("^2[0-9][0-9][0-9]$")
inPatter = re.compile("^([0-9][0-9])in$")
cmPattern = re.compile("^([0-9][0-9][0-9])cm$")
hclPattern = re.compile("^#[0-9a-f]{6}$")
ecls = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
pidPattern = re.compile("^[0-9]{9}$")

def validateItem(key, value):
    result = False
    if key == "cid":
        result = True
    elif key == "byr":
        if byrPattern.match(value):
            val = int(value)
            result = val >= 1920 and val <= 2002
    elif key == "iyr":
        if iyrPattern.match(value):
            val = int(value)
            result = val >= 2010 and val <= 2020
    elif key == "eyr":
        if eyrPattern.match(value):
            val = int(value)
            result = val >= 2020 and val <= 2030
    elif key == "hgt":
        inm = inPatter.match(value)
        cmm = cmPattern.match(value)
        if inm:
            val = int(inm.group(1))
            result = val >= 59 and val <= 76
        elif cmm:
            val = int(cmm.group(1))
            result = val >= 150 and val <= 193
    elif key == "hcl":
        if hclPattern.match(value):
            result = True
    elif key == "ecl":
        result = (value in ecls)
    elif key == "pid":
        if pidPattern.match(value):
            result = True
    else:
        raise UnknownKey

    return result

def isValidItem(item):
    required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    optional = ["cid"]
    valid = True
    for req in required:
        if req not in item:
            valid = False
    for key in item:
        if key not in required and key not in optional:
            raise UnknownKey

    return valid

def isValidItemStrict(item):
    valid = False
    if isValidItem(item):
        valid = True
        for k in item:
            if valid:
                valid = validateItem(k, item[k])
    return valid

if __name__ == "__main__":
    passes = LoadDicts("input/d04.txt")
    valid = 0
    strict = 0
    total = 0
    for p in passes:
        total += 1
        if isValidItem(p):
            valid += 1
        if isValidItemStrict(p):
            strict += 1
    print ("Passports: {0} valid of {1}".format(valid, total))
    print ("Passports strictly valid: {0} valid of {1}".format(strict, total))
