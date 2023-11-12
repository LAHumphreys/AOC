import re

from tools.file_loader import load_dicts


class UnknownKey(Exception):
    pass


BYR_PATTERN = re.compile("^[1-2][0-9][0-9][0-9]$")
IYR_PATTERN = re.compile("^2[0-9][0-9][0-9]$")
EYR_PATTERN = re.compile("^2[0-9][0-9][0-9]$")
IN_PATTERN = re.compile("^([0-9][0-9])in$")
CM_PATTERN = re.compile("^([0-9][0-9][0-9])cm$")
HCL_PATTERN = re.compile("^#[0-9a-f]{6}$")
EYE_COLOUR = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
PID_PATTERN = re.compile("^[0-9]{9}$")

def check_iyr(value):
    result = False
    if IYR_PATTERN.match(value):
        val = int(value)
        result = 2010 <= val <= 2020
    return result


def check_eyr(value):
    result = False
    if EYR_PATTERN.match(value):
        val = int(value)
        result = 2020 <= val <= 2030
    return result


def check_hgt(value):
    result = False
    inm = IN_PATTERN.match(value)
    cmm = CM_PATTERN.match(value)
    if inm:
        val = int(inm.group(1))
        result = 59 <= val <= 76
    elif cmm:
        val = int(cmm.group(1))
        result = 150 <= val <= 193
    return result

def check_byr(value):
    result = False
    if BYR_PATTERN.match(value):
        val = int(value)
        result = 1920 <= val <= 2002
    return result


def validate_item(key, value):
    result = False
    if key == "cid":
        result = True
    elif key == "byr":
        result = check_byr(value)
    elif key == "iyr":
        result = check_iyr(value)
    elif key == "eyr":
        result = check_eyr(value)
    elif key == "hgt":
        result = check_hgt(value)
    elif key == "hcl":
        result = HCL_PATTERN.match(value) is not None
    elif key == "ecl":
        result = value in EYE_COLOUR
    elif key == "pid":
        result = PID_PATTERN.match(value) is not None
    else:
        raise UnknownKey

    return result


def is_valid_item(item):
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


def is_valid_item_strict(item):
    valid = False
    if is_valid_item(item):
        valid = True
        for k in item:
            if valid:
                valid = validate_item(k, item[k])
    return valid


if __name__ == "__main__":
    def main():
        passes = load_dicts("input/d04.txt")
        valid = 0
        strict = 0
        total = 0
        for pass_to_check in passes:
            total += 1
            if is_valid_item(pass_to_check):
                valid += 1
            if is_valid_item_strict(pass_to_check):
                strict += 1
        print("Passports: {0} valid of {1}".format(valid, total))
        print(
            "Passports strictly valid: {0} valid of {1}".format(
                strict, total))

    main()
