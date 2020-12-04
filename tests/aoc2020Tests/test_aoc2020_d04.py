from aoc2020.d04 import isValidItem, UnknownKey, validateItem, isValidItemStrict
from unittest import TestCase
from tools.dictTools import buildDicts
import copy

class Test_ValidPassport(TestCase):
    examples = [{
        "ecl": "gry", "pid": "860033327", "eyr": "2020", "hcl": "#fffffd",
        "byr": "1937", "iyr": "2017", "cid": "147", "hgt": "183cm",
    }, {
        "iyr": "2013", "ecl": "amb", "cid": "350", "eyr": "2023", "pid": "028048884",
        "hcl": "#cfa07d", "byr": "1929",
    }, {
        "hcl": "#ae17e1", "iyr": "2013",
        "eyr": "2024",
        "ecl": "brn", "pid": "760753108", "byr": "1931",
        "hgt": "179cm",
    }, {
        "hcl": "#cfa07d", "eyr": "2025", "pid": "166559648",
        "iyr": "2011", "ecl": "brn", "hgt": "59in",
    }]

    def test_Example1(self):
        self.assertEqual(True, isValidItem(self.examples[0]))

    def test_Example2(self):
        self.assertEqual(False, isValidItem(self.examples[1]))

    def test_Example3(self):
        self.assertEqual(True, isValidItem(self.examples[2]))

    def test_Example4(self):
        self.assertEqual(False, isValidItem(self.examples[3]))

    def test_ExtraItem(self):
        item = copy.copy(self.examples[0])
        item["NotValid"] = "XXX"
        self.assertRaises(UnknownKey, lambda: isValidItem(item))


class Test_Validator(TestCase):

    def test_byr(self):
        self.assertFalse(validateItem("byr", ""))
        self.assertFalse(validateItem("byr", "xxx"))
        self.assertFalse(validateItem("byr", "xxxx"))
        self.assertFalse(validateItem("byr", "1"))
        self.assertFalse(validateItem("byr", "123"))
        self.assertFalse(validateItem("byr", "12"))
        self.assertFalse(validateItem("byr", "12xx"))

        self.assertTrue(validateItem("byr", "1920"))
        self.assertTrue(validateItem("byr", "2002"))

        self.assertFalse(validateItem("byr", "1919"))
        self.assertFalse(validateItem("byr", "2003"))

    def test_iyr(self):
        self.assertFalse(validateItem("iyr", ""))
        self.assertFalse(validateItem("iyr", "xxx"))
        self.assertFalse(validateItem("iyr", "xxxx"))
        self.assertFalse(validateItem("iyr", "1"))
        self.assertFalse(validateItem("iyr", "123"))
        self.assertFalse(validateItem("iyr", "12"))
        self.assertFalse(validateItem("iyr", "12xx"))

        self.assertTrue(validateItem("iyr", "2010"))
        self.assertTrue(validateItem("iyr", "2020"))

        self.assertFalse(validateItem("iyr", "2009"))
        self.assertFalse(validateItem("iyr", "2021"))

    def test_eyr(self):
        self.assertFalse(validateItem("eyr", ""))
        self.assertFalse(validateItem("eyr", "xxx"))
        self.assertFalse(validateItem("eyr", "xxxx"))
        self.assertFalse(validateItem("eyr", "1"))
        self.assertFalse(validateItem("eyr", "123"))
        self.assertFalse(validateItem("eyr", "12"))
        self.assertFalse(validateItem("eyr", "12xx"))

        self.assertTrue(validateItem("eyr", "2020"))
        self.assertTrue(validateItem("eyr", "2030"))

        self.assertFalse(validateItem("eyr", "2019"))
        self.assertFalse(validateItem("eyr", "2031"))

    def test_height(self):
        self.assertFalse(validateItem("hgt", ""))
        self.assertFalse(validateItem("hgt", "xxx"))
        self.assertFalse(validateItem("hgt", "xxxx"))
        self.assertFalse(validateItem("hgt", "123"))

        self.assertTrue(validateItem("hgt", "59in"))
        self.assertTrue(validateItem("hgt", "76in"))
        self.assertFalse(validateItem("hgt", "58in"))
        self.assertFalse(validateItem("hgt", "77in"))

        self.assertTrue(validateItem("hgt", "150cm"))
        self.assertTrue(validateItem("hgt", "193cm"))
        self.assertFalse(validateItem("hgt", "149cm"))
        self.assertFalse(validateItem("hgt", "194cm"))

    def test_hcl(self):
        self.assertTrue(validateItem("hcl", "#123abc"))
        self.assertTrue(validateItem("hcl", "#000000"))
        self.assertTrue(validateItem("hcl", "#ffffff"))

        self.assertFalse(validateItem("hcl", "123abc1"))
        self.assertFalse(validateItem("hcl", "123abc#"))
        self.assertFalse(validateItem("hcl", "#fffffg"))
        self.assertFalse(validateItem("hcl", "#1234567"))

    def test_ecl(self):
        self.assertTrue(validateItem("ecl", "amb"))
        self.assertTrue(validateItem("ecl", "blu"))
        self.assertTrue(validateItem("ecl", "brn"))
        self.assertTrue(validateItem("ecl", "gry"))
        self.assertTrue(validateItem("ecl", "hzl"))
        self.assertTrue(validateItem("ecl", "oth"))

        self.assertFalse(validateItem("ecl", ""))
        self.assertFalse(validateItem("ecl", "xxx"))

    def test_pid(self):
        self.assertTrue(validateItem("pid", "000000001"))
        self.assertTrue(validateItem("pid", "123456789"))

        self.assertFalse(validateItem("pid", "1234567890"))
        self.assertFalse(validateItem("pid", "123a56789"))

    def test_cid(self):
        self.assertTrue(validateItem("cid", ""))
        self.assertTrue(validateItem("cid", "xxx"))
        self.assertTrue(validateItem("cid", "123"))

    def test_unknownKey(self):
        self.assertRaises(UnknownKey, lambda: validateItem("", "xxx"))
        self.assertRaises(UnknownKey, lambda: validateItem("xx", "xxx"))
        self.assertRaises(UnknownKey, lambda: validateItem("pid1", "xxx"))
        self.assertRaises(UnknownKey, lambda: validateItem("2cid", "xxx"))


class Test_StrictValidator(TestCase):
    def test_Example1(self):
        validDefns = """
            pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
            hcl:#623a2f

            eyr:2029 ecl:blu cid:129 byr:1989
            iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

            hcl:#888785
            hgt:164cm byr:2001 iyr:2015 cid:88
            pid:545766238 ecl:hzl
            eyr:2022

            iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
        """
        items = buildDicts(validDefns)
        for i in items:
            self.assertTrue(isValidItemStrict(i))

    def test_Example2(self):
        invalidDefns = """
            eyr:1972 cid:100
            hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

            iyr:2019
            hcl:#602927 eyr:1967 hgt:170cm
            ecl:grn pid:012533040 byr:1946

            hcl:dab227 iyr:2012
            ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

            hgt:59cm ecl:zzz
            eyr:2038 hcl:74454a iyr:2023
            pid:3556412378 byr:2007
        """
        items = buildDicts(invalidDefns)
        for i in items:
            self.assertEqual(False, isValidItemStrict(i))

    def test_MissingItem(self):
        validDefn = """
            pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
            hcl:#623a2f
        """
        item = buildDicts(validDefn)[0]
        self.assertEqual(True, isValidItemStrict(item))
        del item["pid"]
        self.assertEqual(False, isValidItemStrict(item))
