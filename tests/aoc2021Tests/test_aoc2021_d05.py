from unittest import TestCase

from aoc2021.d05 import DirectedVector, Vector, parse_vector, load_part_one, get_vector_overlap, get_all_overlaps, get_intersection
from aoc2021.d05 import remove_overlap, remove_overlaps, remove_all_overlaps, point_count, part_one
from aoc2021.d05 import promote_vector, promote_point, promote_line, part_two, load_part_two, debug_draw
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class TestVectorParsing(TestCase):
    def test_vector_parse(self):
        vector: Vector = parse_vector("928,972 -> 28,72")

        self.assertEqual(vector.x_min, 28)
        self.assertEqual(vector.x_max, 928)
        self.assertEqual(vector.y_min, 72)
        self.assertEqual(vector.y_max, 972)
        self.assertEqual(vector.x_start, 928)
        self.assertEqual(vector.x_end, 28)
        self.assertEqual(vector.y_start, 972)
        self.assertEqual(vector.y_end, 72)

    def test_load_part_one(self):
        vectors = load_part_one(get_test_file_path("samples/d05.txt"))

        self.assertEqual(len(vectors), 6)
        self.assertEqual(vectors[0], DirectedVector(x_min=0, x_max=5, y_min=9, y_max=9, x_start=0, x_end=5, y_start=9, y_end=9))
        self.assertEqual(vectors[1], DirectedVector(x_min=3, x_max=9, y_min=4, y_max=4, x_start=9, x_end=3, y_start=4, y_end=4))
        self.assertEqual(vectors[2], DirectedVector(x_min=2, x_max=2, y_min=1, y_max=2, x_start=2, x_end=2, y_start=2, y_end=1))
        self.assertEqual(vectors[3], DirectedVector(x_min=7, x_max=7, y_min=0, y_max=4, x_start=7, x_end=7, y_start=0, y_end=4))
        self.assertEqual(vectors[4], DirectedVector(x_min=0, x_max=2, y_min=9, y_max=9, x_start=0, x_end=2, y_start=9, y_end=9))
        self.assertEqual(vectors[5], DirectedVector(x_min=1, x_max=3, y_min=4, y_max=4, x_start=3, x_end=1, y_start=4, y_end=4))

    def test_load_part_two(self):
        vectors = load_part_two(get_test_file_path("samples/d05.txt"))

        self.assertEqual(len(vectors), 10)
        self.assertListEqual(vectors,
                             [
                                 promote_line(0, 9, 5, 9),
                                 promote_line(8, 0, 0, 8),
                                 promote_line(9, 4, 3, 4),
                                 promote_line(2, 2, 2, 1),
                                 promote_line(7, 0, 7, 4),
                                 promote_line(6, 4, 2, 0),
                                 promote_line(0, 9, 2, 9),
                                 promote_line(3, 4, 1, 4),
                                 promote_line(0, 0, 8, 8),
                                 promote_line(5, 5, 8, 2)])
        debug_draw(vectors)


class TestOverlap(TestCase):
    def test_no_overlap(self):
        overlaps =[
            get_vector_overlap(promote_vector(Vector(x_min=0, x_max=0, y_min=1, y_max=99)),
                               promote_vector(Vector(x_min=1, x_max=1, y_min=1, y_max=99))),
            get_vector_overlap(promote_vector(Vector(x_min=0, x_max=0, y_min=1, y_max=49)),
                               promote_vector(Vector(x_min=0, x_max=0, y_min=50, y_max=99))),
        ]
        for overlap in overlaps:
            self.assertListEqual(overlap, [])

    def test_no_overlap_sample(self):
        vectors = [promote_line(2,2 , 2,1), promote_line(6,4 , 2,0)]
        debug_draw(vectors)
        overlap = get_vector_overlap(vectors[0], vectors[1])
        self.assertListEqual(overlap, [])

    def test_partial_xy_overlap(self):
        overlap = get_vector_overlap(promote_line(0, 0, 10, 10),
                                     promote_line(2, 2, 8, 8))
        self.assertEqual(overlap, [promote_line(2,2, 8,8)])

    def test_parallel_xy_overlap(self):
        overlap = get_vector_overlap(promote_line(6, 4, 2, 0),
                                     promote_line(0, 0, 8, 8))
        self.assertEqual(overlap, [])

    def test_no_xy_overlap(self):
        overlap = get_vector_overlap(promote_line(0, 0, 5, 5),
                                     promote_line(6, 6, 8, 8))
        self.assertEqual(overlap, [])


    def test_partial_x_overlap(self):
        overlap = get_vector_overlap(promote_vector(Vector(x_min=0, x_max=10, y_min=1, y_max=1)),
                                     promote_vector(Vector(x_min=-2, x_max=12, y_min=1, y_max=1)))
        self.assertEqual(overlap, [promote_vector(Vector(x_min=0, x_max=10, y_min=1, y_max=1))])

    def test_exact_x_overlap(self):
        overlap = get_vector_overlap(promote_vector(Vector(x_min=1, x_max=10, y_min=1, y_max=1)),
                                     promote_vector(Vector(x_min=0, x_max=1, y_min=1, y_max=1)))
        self.assertEqual(overlap, [promote_vector(Vector(x_min=1, x_max=1, y_min=1, y_max=1))])

    def test_exact_xy_overlap(self):
        overlap = get_vector_overlap(promote_line(2, 2, 10, 10), promote_line(0, 0, 2, 2))
        self.assertEqual(overlap, [promote_point(2,2)])


    def test_exact_y_overlap(self):
        overlap = get_vector_overlap(promote_vector(Vector(x_min=1, x_max=1, y_min=1, y_max=2)),
                                     promote_vector(Vector(x_min=1, x_max=1, y_min=2, y_max=10)))
        self.assertEqual(overlap, [promote_vector(Vector(x_min=1, x_max=1, y_min=2, y_max=2))])

    def test_partial_y_overlap(self):
        overlap = get_vector_overlap(promote_vector(Vector(x_min=10, x_max=10, y_min=1, y_max=100)),
                                     promote_vector(Vector(x_min=10, x_max=10, y_min=7, y_max=121)))
        self.assertEqual(overlap, [promote_vector(Vector(x_min=10, x_max=10, y_min=7, y_max=100))])

    def test_sample_overlap(self):
        overlap = get_vector_overlap(promote_vector(Vector(x_min=7, x_max=7, y_min=0, y_max=4)),
                                     promote_vector(Vector(x_min=3, x_max=9, y_min=4, y_max=4)))
        self.assertEqual(overlap, [promote_vector(Vector(x_min=7, x_max=7, y_min=4, y_max=4))])

    def test_cross(self):
        overlap = get_vector_overlap(
            DirectedVector(x_min=0, x_max=8, y_min=0, y_max=8, x_start=8, x_end=0, y_start=0, y_end=8),
            DirectedVector(x_min=0, x_max=8, y_min=0, y_max=8, x_start=0, x_end=8, y_start=0, y_end=8))
        self.assertEqual(overlap, [promote_point(4,4)])

    def test_xy_cross(self):
        overlap = get_vector_overlap(promote_line(0,0, 2, 2), promote_line(0,2, 2, 0))
        self.assertEqual(overlap, [promote_point(1,1)])


class TestIntersection(TestCase):
    def test_intersection(self):
        intersection = get_intersection(promote_line(7,0, 7,4), promote_line(3,4, 9,4))
        self.assertEqual(intersection, [promote_point(7,4)])

    def test_xy_xy_intersection(self):
        intersection = get_intersection(promote_line(0,0,  6,6), promote_line(0,6,  6,0))
        self.assertEqual(intersection, [promote_point(3,3)])

    def test_xy_xy_miss(self):
        intersection = get_intersection(promote_line(0,0,  6,6), promote_line(7,7,  9,9))
        self.assertEqual(intersection, [])

    def test_xy_x_intersection(self):
        # Two INF cases
        intersection_first = get_intersection(promote_line(0,0,  6,6), promote_line(3,0,  3,6))
        intersection_second = get_intersection( promote_line(3,0,  3,6), promote_line(0,0,  6,6))
        self.assertEqual(intersection_first, [promote_point(3,3)])
        self.assertEqual(intersection_second, [promote_point(3,3)])


    def test_xy_y_intersection(self):
        intersection = get_intersection(promote_line(0,0,  6,6), promote_line(0,3,  6,3))
        self.assertEqual(intersection, [promote_point(3,3)])


class GetAllOverlaps(TestCase):
    def test_get_overlaps(self):
        vectors = load_part_one(get_test_file_path("samples/d05.txt"))
        overlaps = get_all_overlaps(vectors)
        print(debug_draw(vectors))
        print(debug_draw(overlaps))
        self.assertListEqual(
            overlaps,
            [
                promote_vector(Vector(x_min=0, x_max=2, y_min=9, y_max=9)),
                promote_vector(Vector(x_min=7, x_max=7, y_min=4, y_max=4)),
                promote_vector(Vector(x_min=3, x_max=3, y_min=4, y_max=4))
            ])


class TestRemoveOverlap(TestCase):
    def test_remove_exact_overlap(self):
        simplified = remove_overlap(
            promote_vector(Vector(x_min=0, x_max=2, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=0, x_max=2, y_min=9, y_max=9))
        )
        self.assertListEqual(simplified, [])

    def test_remove_exact_xy_overlap(self):
        simplified = remove_overlap(promote_line(0, 0, 8, 8), promote_line(0, 0, 8, 8))
        self.assertListEqual(simplified, [])

    def test_x_remove_partial(self):
        simplified = remove_overlap(
            promote_vector(Vector(x_min=0, x_max=10, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=1, x_max=3, y_min=9, y_max=9))
        )
        self.assertListEqual(simplified, [
            promote_vector(Vector(x_min=0, x_max=0, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=4, x_max=10, y_min=9, y_max=9))])

    def test_xy_remove_partial(self):
        simplified = remove_overlap(promote_line(0,0, 10,10), promote_line(2,2, 8,8),)
        self.assertListEqual(simplified, [promote_line(0,0, 1,1), promote_line(9,9, 10,10)])

    def test_x_remove_sub_path(self):
        simplified = remove_overlap(
            promote_vector(Vector(x_min=1, x_max=2, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=1, x_max=3, y_min=9, y_max=9))
        )
        self.assertListEqual(simplified, [])

    def test_y_remove_partial(self):
        simplified = remove_overlap(
            promote_vector(Vector(y_min=0, y_max=10, x_min=9, x_max=9)),
            promote_vector(Vector(y_min=1, y_max=3,  x_min=9, x_max=9))
        )
        self.assertListEqual(simplified, [
            promote_vector(Vector(y_min=0, y_max=0,  x_min=9, x_max=9)),
            promote_vector(Vector(y_min=4, y_max=10, x_min=9, x_max=9))])

    def test_y_remove_sub_path(self):
        simplified = remove_overlap(
            promote_vector(Vector(y_min=1, y_max=2, x_min=9, x_max=9)),
            promote_vector(Vector(y_min=1, y_max=3, x_min=9, x_max=9))
        )
        self.assertListEqual(simplified, [])

    def test_remove_intersection(self):
        simplified = remove_overlap(
            promote_vector(Vector(x_min=1, x_max=9, y_min=5, y_max=5)),
            promote_vector(Vector(x_min=5, x_max=5, y_min=1, y_max=9))
        )
        self.assertListEqual(simplified, [
            promote_vector(Vector(x_min=1, x_max=4,  y_min=5, y_max=5)),
            promote_vector(Vector(x_min=6, x_max=9, y_min=5, y_max=5))])

    def test_remove_exact_overlaps(self):
        simplified = remove_overlaps(
            promote_vector(Vector(x_min=0, x_max=10, y_min=9, y_max=9)),
            [promote_vector(Vector(x_min=0, x_max=2, y_min=9, y_max=9)), promote_vector(Vector(x_min=3, x_max=10, y_min=9, y_max=9))]
        )
        self.assertListEqual(simplified, [])

    def test_x_remove_sub_paths(self):
        simplified = remove_overlaps(
            promote_vector(promote_vector(Vector(x_min=0, x_max=10, y_min=9, y_max=9))),
            [promote_vector(promote_vector(Vector(x_min=1, x_max=3, y_min=9, y_max=9))),
             promote_vector(promote_vector(Vector(x_min=5, x_max=8, y_min=9, y_max=9)))]
        )
        self.assertListEqual(simplified, [
            promote_vector(Vector(x_min=0, x_max=0,  y_min=9, y_max=9)),
            promote_vector(Vector(x_min=4, x_max=4, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=9, x_max=10, y_min=9, y_max=9))])

    def test_xy_remove_sub_paths(self):
        simplified = remove_overlaps(
            promote_line(0,0, 10,10),
            [promote_line(1,1, 3,3), promote_line(6,6, 8,8)])
        self.assertListEqual(simplified, [
            promote_point(0,0),
            promote_line(4,4, 5,5),
            promote_line(9,9, 10,10)])

    def test_remove_all_overlaps(self):
        simplified = remove_all_overlaps(
            [promote_vector(Vector(x_min=0, x_max=10, y_min=9, y_max=9)),
             promote_vector(Vector(x_min=1, x_max=3, y_min=9, y_max=9)),
             promote_vector(Vector(x_min=5, x_max=8, y_min=9, y_max=9))]
        )
        expected = [
            promote_vector(Vector(x_min=0, x_max=0,  y_min=9, y_max=9)),
            promote_vector(Vector(x_min=1, x_max=3, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=4, x_max=4, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=5, x_max=8, y_min=9, y_max=9)),
            promote_vector(Vector(x_min=9, x_max=10, y_min=9, y_max=9))]

        simplified.sort(key=lambda v: v.x_min)
        expected.sort(key=lambda v: v.x_min)
        self.assertListEqual(simplified, expected)


class Length(TestCase):
    def test_point(self):
        point: Vector = Vector(x_min=1, x_max=1, y_min=1, y_max=1)
        self.assertEqual(point_count(point), 1)

    def test_x_line(self):
        point: Vector = Vector(x_min=0, x_max=2, y_min=1, y_max=1)
        self.assertEqual(point_count(point), 3)

    def test_y_line(self):
        point: Vector = Vector(x_min=9, x_max=9, y_min=0, y_max=2)
        self.assertEqual(point_count(point), 3)

    def test_xy_line(self):
        point: Vector = Vector(x_min=0, x_max=3, y_min=0, y_max=3)
        self.assertEqual(point_count(point), 4)


class PartOne(TestCase):
    def test_example(self):
        self.assertEqual(part_one(get_test_file_path("samples/d05.txt")), 5)

class PartTwo(TestCase):
    def test_example(self):
        debug_draw(load_part_two("samples/d05.txt"))
        self.assertEqual(part_two(get_test_file_path("samples/d05.txt")), 12)
