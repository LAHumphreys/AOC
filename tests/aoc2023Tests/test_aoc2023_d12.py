from unittest import TestCase

from aoc2023.d12 import spring_possibilities, trim_groups, load_springs, part_one, SpringMap, expand_spring
from aoc2023.d12 import part_two, count_possibilities, subtract_groups
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestTrimGroups(TestCase):
    def test_no_trim(self):
        self.assertListEqual(trim_groups(".....", [1, 2, 3]), [1, 2, 3])

    def test_all_groups(self):
        self.assertListEqual(trim_groups(".#.##.###", [1, 2, 3]), [])

    def test_trim_2_groups(self):
        self.assertListEqual(trim_groups(".#..##..", [1, 2, 3]), [3])

    def test_trim_partial_group(self):
        self.assertListEqual(trim_groups(".#..##..##", [1, 2, 4]), [2])

    def test_trim_multi_groups(self):
        self.assertListEqual(trim_groups("#.#", [1, 1, 3]), [3])

    def test_trim_single_hash(self):
        self.assertListEqual(trim_groups("#", [1, 3]), [3])

    def test_trim_reduce_ingle_hash(self):
        self.assertListEqual(trim_groups("#", [3]), [2])

    def test_trim_reduce_trailing_group(self):
        self.assertListEqual(trim_groups("....#", [1, 1, 3]), [1, 3])

    def test_trim_reduce_trailing_large_group(self):
        self.assertListEqual(trim_groups("....#", [3, 1, 3]), [2, 1, 3])
class TestGeneration(TestCase):

    def test_unique(self):
        expected = ["#.#.###"]
        self.assertListEqual(
            [x for x in spring_possibilities("#.#.###", [1, 1, 3])],
            expected)



    def test_invalid_group_too_small(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.#.###", [1, 2, 3])],
            [])


    def test_invalid_group_too_large(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.#.###", [1, 1, 2])],
            [])

    def test_extra_group(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.#.###.#.", [1, 1, 3])],
            [])
    def test_missing_group(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.#..", [1, 1, 3])],
            [])

    def test_unique_from_unknowns(self):
        # ???.### 1,1,3
        self.assertListEqual(
            [x for x in spring_possibilities("???.###", [1, 1, 3])],
            ["#.#.###"])



    def test_unique_from_single_unknown(self):
        self.assertListEqual(
                [x for x in spring_possibilities("#.?.###", [1, 1, 3])],
                ["#.#.###"])

    def test_intermediary_group_blocks(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.##.#.#.##.", [1, 2, 1, 2])],
            [])

    def test_intermediary_group_too_bigblocks(self):
        self.assertListEqual(
            [x for x in spring_possibilities("#.###.#.##.", [1, 2, 1, 2])],
            [])

    def test_example_2(self):
        print([x for x in spring_possibilities(".??..??...?##.", [1, 1, 3])])
        self.assertEqual(len([x for x in spring_possibilities(".??..??...?##.", [1, 1, 3])]), 4)


    def test_expand(self):
        short = SpringMap(row="???.###", groups=[1,1,3])
        expanded = expand_spring(short)
        self.assertEqual(expanded.row, "???.###????.###????.###????.###????.###")
        self.assertEqual(expanded.groups, [1,1,3,1,1,3,1,1,3,1,1,3,1,1,3])
    def test_example_2_expanded(self):
        short = SpringMap(row=".??..??...?##.", groups=[1, 1, 3])
        expanded = expand_spring(short)
        self.assertEqual(sum([1 for _ in spring_possibilities(expanded.row, expanded.groups)]), 16384)

    def test_example_3(self):
        self.assertEqual(len([x for x in spring_possibilities("?#?#?#?#?#?#?#?", [1,3,1,6])]), 1)

    def test_example_4(self):
        self.assertEqual(len([x for x in spring_possibilities("????.#...#...", [4,1,1])]), 1)

    def test_example_5(self):
        self.assertEqual(len([x for x in spring_possibilities("????.######..#####.", [1,6,5])]), 4)

    def test_example_6(self):
        self.assertEqual(len([x for x in spring_possibilities("?###????????", [3,2,1])]), 10)

class TestLoad(TestCase):
    def test_load_values(self):
        springs = load_springs(get_test_file_path("samples/d12.txt"))
        self.assertListEqual(springs[0].groups, [1, 1, 3])
        self.assertEqual(springs[0].row, "???.###")

    def test_load_last_value(self):
        springs = load_springs(get_test_file_path("samples/d12.txt"))
        self.assertListEqual(springs[-1].groups, [3, 2, 1])
        self.assertEqual(springs[-1].row, "?###????????")

class TestProblem(TestCase):
    def test_part_one(self):
        springs = load_springs(get_test_file_path("samples/d12.txt"))
        self.assertEqual(part_one(springs), 21)

    def test_part_two(self):
        springs = load_springs(get_test_file_path("samples/d12.txt"))
        self.assertEqual(part_two(springs), 525152)


class TestGroupMath(TestCase):
    def test_no_trail_group(self):
        self.assertListEqual(subtract_groups([1, 2, 3], []), [1, 2, 3])

    def test_all_trail_groups(self):
        self.assertListEqual(subtract_groups([1, 2, 3], [1, 2, 3]), [])

    def test_some_groups(self):
        self.assertListEqual(subtract_groups([1, 2, 3], [2, 3]), [1])

    def test_partial_group(self):
        self.assertListEqual(subtract_groups([1, 2, 3], [1, 3]), [1, 1])

    def test_unit_group(self):
        self.assertListEqual(subtract_groups([1, 1, 3], [3]), [1, 1])

class TestCount(TestCase):
    def test_unique_from_unknowns_count(self):
        # ???.### 1,1,3
        self.assertEqual(count_possibilities("???.###", [1, 1, 3]), 1)

    def test_unique_from_unknown_count(self):
        self.assertEqual(count_possibilities("#.?.###", [1, 1, 3]), 1)
    def test_unique_count(self):
        self.assertEqual(count_possibilities("#.#.###", [1, 1, 3]), 1)


    def test_double_unknown(self):
        self.assertEqual(count_possibilities("#.??", [1, 1]), 2)
    def test_tripple_unknown(self):
        self.assertEqual(count_possibilities("#.???", [1, 1]), 3)

    def test_invalid_group_too_small_count(self):
        self.assertEqual(count_possibilities("#.#.###", [1, 2, 3]), 0)

    def test_invalid_group_to_many_count(self):
        self.assertEqual(count_possibilities("?.###", [1, 1, 3]), 0)
    def test_trail_group_prefix(self):
        self.assertEqual(count_possibilities(".....?##.", [3]), 1)
    def test_example2(self):
        self.assertEqual(count_possibilities(".??..??...?##.", [1, 1, 3]), 4)

    def test_example_3_count(self):
        self.assertEqual(count_possibilities("?#?#?#?#?#?#?#?", [1, 3, 1, 6]), 1)

    def test_example_4(self):
        self.assertEqual(count_possibilities("????.#...#...", [4, 1, 1]), 1)

    def test_example_5(self):
        self.assertEqual(count_possibilities("????.######..#####.", [1, 6, 5]), 4)

    def test_example_6(self):
        self.assertEqual(count_possibilities("?###????????", [3, 2, 1]), 10)

    def test_example_6_reduced(self):
        self.assertEqual(count_possibilities(".###.????", [3, 2, 1]), 1)

    def test_pair(self):
        self.assertEqual(count_possibilities("#?", [1, 1]), 0)

    def test_starting_question_hash(self):
        self.assertEqual(count_possibilities("?###.??", [3,2]), 1)