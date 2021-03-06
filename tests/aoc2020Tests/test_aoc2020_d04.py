import copy
from unittest import TestCase

from aoc2020.d04 import is_valid_item, UnknownKey, validate_item, is_valid_item_strict
from tools.dictionary_tools import build_dicts


class Test_ValidPassport(TestCase):
    examples = [{"ecl": "gry",
                 "pid": "860033327",
                 "eyr": "2020",
                 "hcl": "#fffffd",
                 "byr": "1937",
                 "iyr": "2017",
                 "cid": "147",
                 "hgt": "183cm",
                 },
                {"iyr": "2013",
                 "ecl": "amb",
                 "cid": "350",
                 "eyr": "2023",
                 "pid": "028048884",
                 "hcl": "#cfa07d",
                 "byr": "1929",
                 },
                {"hcl": "#ae17e1",
                 "iyr": "2013",
                 "eyr": "2024",
                 "ecl": "brn",
                 "pid": "760753108",
                 "byr": "1931",
                 "hgt": "179cm",
                 },
                {"hcl": "#cfa07d",
                 "eyr": "2025",
                 "pid": "166559648",
                 "iyr": "2011",
                 "ecl": "brn",
                 "hgt": "59in",
                 }]

    def test_Example1(self):
        self.assertEqual(True, is_valid_item(self.examples[0]))

    def test_Example2(self):
        self.assertEqual(False, is_valid_item(self.examples[1]))

    def test_Example3(self):
        self.assertEqual(True, is_valid_item(self.examples[2]))

    def test_Example4(self):
        self.assertEqual(False, is_valid_item(self.examples[3]))

    def test_ExtraItem(self):
        item = copy.copy(self.examples[0])
        item["NotValid"] = "XXX"
        self.assertRaises(UnknownKey, lambda: is_valid_item(item))


class Test_Validator(TestCase):

    def test_byr(self):
        self.assertFalse(validate_item("byr", ""))
        self.assertFalse(validate_item("byr", "xxx"))
        self.assertFalse(validate_item("byr", "xxxx"))
        self.assertFalse(validate_item("byr", "1"))
        self.assertFalse(validate_item("byr", "123"))
        self.assertFalse(validate_item("byr", "12"))
        self.assertFalse(validate_item("byr", "12xx"))

        self.assertTrue(validate_item("byr", "1920"))
        self.assertTrue(validate_item("byr", "2002"))

        self.assertFalse(validate_item("byr", "1919"))
        self.assertFalse(validate_item("byr", "2003"))

    def test_iyr(self):
        self.assertFalse(validate_item("iyr", ""))
        self.assertFalse(validate_item("iyr", "xxx"))
        self.assertFalse(validate_item("iyr", "xxxx"))
        self.assertFalse(validate_item("iyr", "1"))
        self.assertFalse(validate_item("iyr", "123"))
        self.assertFalse(validate_item("iyr", "12"))
        self.assertFalse(validate_item("iyr", "12xx"))

        self.assertTrue(validate_item("iyr", "2010"))
        self.assertTrue(validate_item("iyr", "2020"))

        self.assertFalse(validate_item("iyr", "2009"))
        self.assertFalse(validate_item("iyr", "2021"))

    def test_eyr(self):
        self.assertFalse(validate_item("eyr", ""))
        self.assertFalse(validate_item("eyr", "xxx"))
        self.assertFalse(validate_item("eyr", "xxxx"))
        self.assertFalse(validate_item("eyr", "1"))
        self.assertFalse(validate_item("eyr", "123"))
        self.assertFalse(validate_item("eyr", "12"))
        self.assertFalse(validate_item("eyr", "12xx"))

        self.assertTrue(validate_item("eyr", "2020"))
        self.assertTrue(validate_item("eyr", "2030"))

        self.assertFalse(validate_item("eyr", "2019"))
        self.assertFalse(validate_item("eyr", "2031"))

    def test_height(self):
        self.assertFalse(validate_item("hgt", ""))
        self.assertFalse(validate_item("hgt", "xxx"))
        self.assertFalse(validate_item("hgt", "xxxx"))
        self.assertFalse(validate_item("hgt", "123"))

        self.assertTrue(validate_item("hgt", "59in"))
        self.assertTrue(validate_item("hgt", "76in"))
        self.assertFalse(validate_item("hgt", "58in"))
        self.assertFalse(validate_item("hgt", "77in"))

        self.assertTrue(validate_item("hgt", "150cm"))
        self.assertTrue(validate_item("hgt", "193cm"))
        self.assertFalse(validate_item("hgt", "149cm"))
        self.assertFalse(validate_item("hgt", "194cm"))

    def test_hcl(self):
        self.assertTrue(validate_item("hcl", "#123abc"))
        self.assertTrue(validate_item("hcl", "#000000"))
        self.assertTrue(validate_item("hcl", "#ffffff"))

        self.assertFalse(validate_item("hcl", "123abc1"))
        self.assertFalse(validate_item("hcl", "123abc#"))
        self.assertFalse(validate_item("hcl", "#fffffg"))
        self.assertFalse(validate_item("hcl", "#1234567"))

    def test_ecl(self):
        self.assertTrue(validate_item("ecl", "amb"))
        self.assertTrue(validate_item("ecl", "blu"))
        self.assertTrue(validate_item("ecl", "brn"))
        self.assertTrue(validate_item("ecl", "gry"))
        self.assertTrue(validate_item("ecl", "hzl"))
        self.assertTrue(validate_item("ecl", "oth"))

        self.assertFalse(validate_item("ecl", ""))
        self.assertFalse(validate_item("ecl", "xxx"))

    def test_pid(self):
        self.assertTrue(validate_item("pid", "000000001"))
        self.assertTrue(validate_item("pid", "123456789"))

        self.assertFalse(validate_item("pid", "1234567890"))
        self.assertFalse(validate_item("pid", "123a56789"))

    def test_cid(self):
        self.assertTrue(validate_item("cid", ""))
        self.assertTrue(validate_item("cid", "xxx"))
        self.assertTrue(validate_item("cid", "123"))

    def test_unknownKey(self):
        self.assertRaises(UnknownKey, lambda: validate_item("", "xxx"))
        self.assertRaises(UnknownKey, lambda: validate_item("xx", "xxx"))
        self.assertRaises(UnknownKey, lambda: validate_item("pid1", "xxx"))
        self.assertRaises(UnknownKey, lambda: validate_item("2cid", "xxx"))


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
        items = build_dicts(validDefns)
        for i in items:
            self.assertTrue(is_valid_item_strict(i))

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
        items = build_dicts(invalidDefns)
        for i in items:
            self.assertEqual(False, is_valid_item_strict(i))

    def test_MissingItem(self):
        validDefn = """
            pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
            hcl:#623a2f
        """
        item = build_dicts(validDefn)[0]
        self.assertEqual(True, is_valid_item_strict(item))
        del item["pid"]
        self.assertEqual(False, is_valid_item_strict(item))
