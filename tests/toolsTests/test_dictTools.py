from tools.dictTools import buildDicts
from unittest import TestCase

class Test_DictParser(TestCase):
    def test_oneLine(self):
        defn = "a:b cc:d eee:fff 1:2"
        expected = [{
            "a" : "b",
            "cc": "d",
            "eee": "fff",
            "1": "2",
        }]
        self.assertListEqual(expected, buildDicts(defn))

    def test_multiLine(self):
        defn = """
           a:b cc:d
           eee:fff
           1:2"""
        expected = [{
            "a" : "b",
            "cc": "d",
            "eee": "fff",
            "1": "2",
        }]
        self.assertListEqual(expected, buildDicts(defn))

    def test_multiLine_2Dicts(self):
        defn = """
           a:b cc:d
           
           eee:fff gg:h
           1:2"""
        expected = [{
            "a" : "b",
            "cc": "d"
        }, {
            "eee": "fff",
            "gg": "h",
            "1": "2",
        }]
        self.assertListEqual(expected, buildDicts(defn))


    def test_multiLine_Example(self):
        defn = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
        expected = [{
            "ecl":"gry", "pid":"860033327", "eyr":"2020", "hcl":"#fffffd",
            "byr":"1937", "iyr":"2017", "cid":"147", "hgt":"183cm",
        }, {
            "iyr":"2013", "ecl":"amb", "cid":"350", "eyr":"2023", "pid":"028048884",
            "hcl":"#cfa07d", "byr":"1929",
        }, {
            "hcl":"#ae17e1", "iyr":"2013",
            "eyr":"2024",
            "ecl":"brn", "pid":"760753108", "byr":"1931",
            "hgt":"179cm",
        }, {
            "hcl":"#cfa07d", "eyr":"2025", "pid":"166559648",
            "iyr":"2011", "ecl":"brn", "hgt":"59in",
        }]

        result = buildDicts(defn)
        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertDictEqual(expected[i], result[i])
        self.assertListEqual(expected, buildDicts(defn))

    def test_allowBlank (self):
        defn = "a:b cc: eee:fff 1:2"
        expected = [{
            "a" : "b",
            "cc": "",
            "eee": "fff",
            "1": "2",
        }]
        self.assertListEqual(expected, buildDicts(defn))

    def test_WrongParts_Extra(self):
        defn = "a:b cc:d:xxx eee:fff 1:2"
        self.assertRaises(ValueError, lambda: buildDicts(defn))

    def test_WrongParts_Missing(self):
        defn = "a:b eee 1:2"
        self.assertRaises(ValueError, lambda: buildDicts(defn))
