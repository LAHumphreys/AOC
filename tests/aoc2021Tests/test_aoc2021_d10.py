from unittest import TestCase

from tests.aoc2021Tests.aoc2021_common import get_test_file_path
from aoc2021.d10 import find_err_index, load_code, part_one
from aoc2021.d10 import complete_line, part_two, score_part_2


class CorruptDetector(TestCase):
    def test_valid_snippets(self):
        self.assertEqual(find_err_index("()"), -1)
        self.assertEqual(find_err_index("([])"), -1)
        self.assertEqual(find_err_index("{([])}"), -1)
        self.assertEqual(find_err_index("{()()()}"), -1)
        self.assertEqual(find_err_index("<([{}])>"), -1)
        self.assertEqual(find_err_index("[<>({}){}[([])<>]]"), -1)
        self.assertEqual(find_err_index("(((((((((())))))))))"), -1)

    def test_ignore_trailing(self):
        self.assertEqual(find_err_index("[(()[<>])]({[<{<<[]>>("), -1)

    def test_invalid_case_1(self):
        code = "{([(<{}[<>[]}>{[]{[(<()>"
        index = find_err_index(code)
        self.assertGreater(index, -1)
        self.assertEqual(code[index], "}")

    def test_invalid_case_2(self):
        code = "[[<[([]))<([[{}[[()]]]"
        index = find_err_index(code)
        self.assertGreater(index, -1)
        self.assertEqual(code[index], ")")

    def test_invalid_case_3(self):
        code = "[{[{({}]{}}([{[{{{}}([]"
        index = find_err_index(code)
        self.assertGreater(index, -1)
        self.assertEqual(code[index], "]")

    def test_invalid_case_4(self):
        code = "[<(<(<(<{}))><([]([]()"
        index = find_err_index(code)
        self.assertGreater(index, -1)
        self.assertEqual(code[index], ")")

    def test_invalid_case_5(self):
        code = "<{([([[(<>()){}]>(<<{{"
        index = find_err_index(code)
        self.assertGreater(index, -1)
        self.assertEqual(code[index], ">")

    def test_load_sample(self):
        program = load_code(get_test_file_path("samples/d10.txt"))
        expected_program = [
            "[({(<(())[]>[[{[]{<()<>>",
            "[(()[<>])]({[<{<<[]>>(",
            "{([(<{}[<>[]}>{[]{[(<()>",
            "(((({<>}<{<{<>}{[]{[]{}",
            "[[<[([]))<([[{}[[()]]]",
            "[{[{({}]{}}([{[{{{}}([]",
            "{<[[]]>}<{[{[{[]{()[[[]",
            "[<(<(<(<{}))><([]([]()",
            "<{([([[(<>()){}]>(<<{{",
            "<{([{{}}[<[[[<>{}]]]>[]]"
        ]
        self.assertListEqual(expected_program, program)

    def test_part_one(self):
        program = load_code(get_test_file_path("samples/d10.txt"))
        self.assertEqual(part_one(program), 26397)

class Completor(TestCase):
    def test_complete_code(self):
        self.assertListEqual(complete_line("()"), [])
        self.assertListEqual(complete_line("([])"), [])
        self.assertListEqual(complete_line("{([])}"), [])
        self.assertListEqual(complete_line("{()()()}"), [])
        self.assertListEqual(complete_line("<([{}])>"), [])
        self.assertListEqual(complete_line("[<>({}){}[([])<>]]"), [])
        self.assertListEqual(complete_line("(((((((((())))))))))"), [])

    def test_complete_sample_one(self):
        self.assertListEqual(complete_line("[({(<(())[]>[[{[]{<()<>>"), [c for c in "}}]])})]"])
        self.assertListEqual(complete_line("[(()[<>])]({[<{<<[]>>("), [c for c in ")}>]})"])
        self.assertListEqual(complete_line("(((({<>}<{<{<>}{[]{[]{}"), [c for c in "}}>}>))))"])
        self.assertListEqual(complete_line("{<[[]]>}<{[{[{[]{()[[[]"), [c for c in "]]}}]}]}>"])
        self.assertListEqual(complete_line("<{([{{}}[<[[[<>{}]]]>[]]"), [c for c in "])}>"])

    def test_score_part_two(self):
        self.assertEqual(score_part_2("}}]])})]"), 288957)
        self.assertEqual(score_part_2(")}>]})"), 5566)
        self.assertEqual(score_part_2("}}>}>))))"), 1480781)
        self.assertEqual(score_part_2("]]}}]}]}>"), 995444)
        self.assertEqual(score_part_2("])}>"), 294)

    def test_part_two(self):
        program = load_code(get_test_file_path("samples/d10.txt"))
        self.assertEqual(part_two(program), 288957)
