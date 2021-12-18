from unittest import TestCase

from aoc2021.d18 import encode_to_nodes, decode_to_lists, add, find_first_at_depth
from aoc2021.d18 import reduce, full_reduce, load_snail_numbers, sn_sum, magnitude, largest_magnitude
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Parser(TestCase):
    def test_encode_decode_single(self):
        sn = encode_to_nodes([1, 2])
        self.assertListEqual(decode_to_lists(sn), [1, 2])

    def test_depth_single(self):
        sn = encode_to_nodes([1, 2])
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 1)

    def test_encode_decode_single_embed(self):
        sn = encode_to_nodes([[1,2],3])
        self.assertListEqual(decode_to_lists(sn), [[1,2],3])

    def test_depth_single_embded(self):
        sn = encode_to_nodes([[1, 2], 3])
        self.assertEqual(sn.left_depth, 2)
        self.assertEqual(sn.right_depth, 1)

    def test_encode_decode_complex(self):
        sn = encode_to_nodes([[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]])
        self.assertListEqual(decode_to_lists(sn), [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]])

    def test_depth_complex(self):
        raw_sn = \
            [
                [ # Left
                    [
                        [1, 3],
                        [5, 3]
                    ],
                    [
                        [1, 3],
                        [8, 7]
                    ]
                ],
                [ # Right
                    [4, 9],
                    [6, 9]
                ]
            ]
        sn = encode_to_nodes(raw_sn)
        self.assertEqual(sn.left_depth, 4)
        self.assertEqual(sn.right_depth, 3)


class Addition(TestCase):
    def test_simple_add(self):
        left = encode_to_nodes([1, 2])
        right = encode_to_nodes([[3, 4], 5])
        result = add(left, right)
        expected =\
            [
                [1,2], # Left
                [      # Right
                    [3,4],
                    5
                ]
            ]
        self.assertListEqual(decode_to_lists(result), expected)
        self.assertEqual(result.left_depth, 2)
        self.assertEqual(result.right_depth, 3)


class Reduction(TestCase):
    def test_find_at_depth_none(self):
        self.assertIsNone(find_first_at_depth(encode_to_nodes([1,2]), 5))
        self.assertIsNone(find_first_at_depth(encode_to_nodes([[1,2], 3]), 5))
        self.assertIsNone(find_first_at_depth(encode_to_nodes([[1,9],[8,5]]), 5))
        self.assertIsNone(find_first_at_depth(encode_to_nodes([[[[1,2],[3,4]],[[5,6],[7,8]]],9]), 5))

    def test_find_at_depth_example_one(self):
        sn = encode_to_nodes([[[[[9,8],1],2],3],4])
        to_explode = find_first_at_depth(sn, 5)
        self.assertListEqual(decode_to_lists(to_explode), [9, 8])

    def test_find_at_depth_example_two(self):
        sn = encode_to_nodes([7,[6,[5,[4,[3,2]]]]])
        to_explode = find_first_at_depth(sn, 5)
        self.assertListEqual(decode_to_lists(to_explode), [3, 2])

    def test_find_at_depth_other_examples_two(self):
        test_cases = [
            ([[6,[5,[4,[3,2]]]],1], [3,2]),
            ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [7, 3]),
            ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [7, 3]),
            ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [3, 2])
        ]
        for raw_sn, expected in test_cases:
            sn = encode_to_nodes(raw_sn)
            to_explode = find_first_at_depth(sn, 5)
            self.assertListEqual(decode_to_lists(to_explode), expected)


    def test_no_reduction(self):
        sn = encode_to_nodes([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9])
        reduce(sn)
        self.assertEqual(decode_to_lists(sn), [[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9])

    def test_reduce_example_one(self):
        sn = encode_to_nodes([[[[[9,8],1],2],3],4])
        self.assertEqual(sn.left_depth, 5)
        self.assertEqual(sn.right_depth, 1)
        reduce(sn)
        self.assertListEqual(decode_to_lists(sn), [[[[0,9],2],3],4])
        self.assertEqual(sn.left_depth, 4)
        self.assertEqual(sn.right_depth, 1)

    def test_reduce_example_two(self):
        sn = encode_to_nodes([7,[6,[5,[4,[3,2]]]]])
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 5)
        reduce(sn)
        self.assertListEqual(decode_to_lists(sn), [7,[6,[5,[7,0]]]])
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 4)

    def test_reduce_other_examples(self):
        test_cases = [
            ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
            ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]])
        ]
        for raw_sn, expected in test_cases:
            sn = encode_to_nodes(raw_sn)
            reduce(sn)
            self.assertListEqual(decode_to_lists(sn), expected)

    def test_reduce_complex_example_rightwards(self):
        raw_sn = [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]
        expected = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]

        sn = encode_to_nodes(raw_sn)
        reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)

    def test_simple_splits_left(self):
        raw_sn = [11, 1]
        expected = [[5, 6], 1]

        sn = encode_to_nodes(raw_sn)
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 1)

        reduce(sn)
        self.assertEqual(sn.left_depth, 2)
        self.assertEqual(sn.right_depth, 1)

        self.assertListEqual(decode_to_lists(sn), expected)

    def test_simple_splits_right(self):
        raw_sn = [1, 11]
        expected = [1, [5, 6]]

        sn = encode_to_nodes(raw_sn)
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 1)

        reduce(sn)
        self.assertEqual(sn.left_depth, 1)
        self.assertEqual(sn.right_depth, 2)

        self.assertListEqual(decode_to_lists(sn), expected)

    def test_example_split_one(self):
        raw_sn = [[[[0,7],4],[15,[0,13]]],[1,1]]
        expected = [[[[0,7],4],[[7,8],[0,13]]],[1,1]]

        sn = encode_to_nodes(raw_sn)
        reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)

    def test_example_split_two(self):
        raw_sn = [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
        expected = [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

        sn = encode_to_nodes(raw_sn)
        reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)

    def test_full_reduce_one_step(self):
        raw_sn=[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
        expected = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

        sn = encode_to_nodes(raw_sn)
        full_reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)

    def test_full_reduce_two_steps(self):
        raw_sn=[[[[0,7],4],[[7,8],[0,13]]],[1,1]]
        expected = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

        sn = encode_to_nodes(raw_sn)
        full_reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)

    def test_full_reduce(self):
        raw_sn=[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
        expected = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

        sn = encode_to_nodes(raw_sn)
        full_reduce(sn)
        self.assertListEqual(decode_to_lists(sn), expected)


class Magnitude(TestCase):
    def test_sample_one(self):
        self.assertEqual(magnitude(encode_to_nodes([[1,2],[[3,4],5]])), 143)

    def test_sample_two(self):
        self.assertEqual(magnitude(encode_to_nodes([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])), 3488)


class SumExamples(TestCase):
    def test_sample_one(self):
        numbers = load_snail_numbers(get_test_file_path("samples/d18/sample1.txt"))
        expected = [[[[1,1],[2,2]],[3,3]],[4,4]]
        total = sn_sum(numbers)
        self.assertEqual(decode_to_lists(total), expected)

    def test_sample_two(self):
        numbers = load_snail_numbers(get_test_file_path("samples/d18/sample2.txt"))
        expected = [[[[3,0],[5,3]],[4,4]],[5,5]]
        total = sn_sum(numbers)
        self.assertEqual(decode_to_lists(total), expected)

    def test_sample_three(self):
        numbers = load_snail_numbers(get_test_file_path("samples/d18/sample3.txt"))
        expected = [[[[5,0],[7,4]],[5,5]],[6,6]]
        total = sn_sum(numbers)
        self.assertEqual(decode_to_lists(total), expected)

    def test_sample_four(self):
        numbers = load_snail_numbers(get_test_file_path("samples/d18/sample4.txt"))
        expected = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
        total = sn_sum(numbers)
        self.assertEqual(decode_to_lists(total), expected)

    def test_largest_magnitude(self):
        numbers = load_snail_numbers(get_test_file_path("samples/d18/sample5.txt"))
        self.assertEqual(largest_magnitude(numbers), 3993)

