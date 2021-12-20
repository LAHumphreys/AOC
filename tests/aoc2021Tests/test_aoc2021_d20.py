from unittest import TestCase

from aoc2021.d20 import convert_pixels_to_int, load_image, get_pixel, get_algo_index_for_pixel
from aoc2021.d20 import enhance, count_lit_pixels, recusive_enhance
from tests.aoc2021Tests.aoc2021_common import get_test_file_path

class Loader(TestCase):
    def test_algo(self):
        algo, _ = load_image(get_test_file_path("samples/d20.txt"))
        self.assertEqual(algo.pixel_map[0], ".")
        self.assertEqual(algo.pixel_map[511], "#")
        self.assertEqual(algo.pixel_map[34], "#")

    def test_image(self):
        _, image = load_image(get_test_file_path("samples/d20.txt"))
        expected_image = ["#..#.", "#....", "##..#", "..#..", "..###"]
        self.assertListEqual(expected_image, image.pixels)
        self.assertEqual(5, image.height)
        self.assertEqual(5, image.width)
        self.assertEqual(".", image.infinity_pixel)



class Indexer(TestCase):
    def test_binary_conversion(self):
        self.assertEqual(convert_pixels_to_int("........."), 0)
        self.assertEqual(convert_pixels_to_int("#########"), 511)



class Indexer(TestCase):
    def test_binary_conversion(self):
        self.assertEqual(convert_pixels_to_int("........."), 0)
        self.assertEqual(convert_pixels_to_int("#########"), 511)
        self.assertEqual(convert_pixels_to_int("...#...#."), 34)

    def test_pixel_indexer(self):
        _, image = load_image(get_test_file_path("samples/d20.txt"))
        self.assertEqual(get_pixel(image, -1, 0), ".")
        self.assertEqual(get_pixel(image, 5, 0), ".")
        self.assertEqual(get_pixel(image, 0, 5), ".")
        self.assertEqual(get_pixel(image, 0, 0), "#")
        self.assertEqual(get_pixel(image, 4, 4), "#")
        self.assertEqual(get_pixel(image, 2, 3), "#")

    def test_get_map_index(self):
        _, image = load_image(get_test_file_path("samples/d20.txt"))
        self.assertEqual(get_algo_index_for_pixel(image, 2, 2), 34)
        self.assertEqual(get_algo_index_for_pixel(image, 0, 0), convert_pixels_to_int("....#..#."))
        self.assertEqual(get_algo_index_for_pixel(image, -3, -3), 0)

    def test_get_map_infinitiy(self):
        _, image = load_image(get_test_file_path("samples/d20.txt"))
        self.assertEqual(get_algo_index_for_pixel(image, -3, -3), 0)
        image.infinity_pixel = "#"
        self.assertEqual(get_algo_index_for_pixel(image, -3, -3), 511)


class Enhancer(TestCase):
    def test_one_step(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        enhanced = enhance(image, algo)
        expected = [
            ".........",
            "..##.##..",
            ".#..#.#..",
            ".##.#..#.",
            ".####..#.",
            "..#..##..",
            "...##..#.",
            "....#.#..",
            "........."
        ]
        self.assertEqual(enhanced.infinity_pixel, ".")
        self.assertListEqual(enhanced.pixels, expected)

    def test_two_steps(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        enhanced = enhance(image, algo)
        enhanced = enhance(enhanced, algo)
        expected = [
            ".............",
            ".............",
            ".........#...",
            "...#..#.#....",
            "..#.#...###..",
            "..#...##.#...",
            "..#.....#.#..",
            "...#.#####...",
            "....#.#####..",
            ".....##.##...",
            "......###....",
            ".............",
            ".............",

        ]
        self.assertEqual(enhanced.infinity_pixel, ".")
        self.assertListEqual(enhanced.pixels, expected)

    def test_infinity_flip(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        algo.pixel_map = "#" + algo.pixel_map[1:]
        algo.pixel_map = algo.pixel_map[0:-1] + "."
        enhanced = enhance(image, algo)
        enhanced_again = enhance(enhanced, algo)
        self.assertEqual(enhanced.infinity_pixel, "#")
        self.assertEqual(enhanced_again.infinity_pixel, ".")

    def test_count_lit_pixels(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        enhanced = enhance(image, algo)
        enhanced_again = enhance(enhanced, algo)
        self.assertEqual(count_lit_pixels(enhanced_again), 35)

    def test_recursive_enhance(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        enhanced = recusive_enhance(image, algo, 2)
        self.assertEqual(count_lit_pixels(enhanced), 35)

    def test_recursive_enhance_part_2(self):
        algo, image = load_image(get_test_file_path("samples/d20.txt"))
        enhanced = recusive_enhance(image, algo, 50)
        self.assertEqual(count_lit_pixels(enhanced), 3351)
