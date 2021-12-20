from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class EnhancementAlgo:
    pixel_map: str


@dataclass
class Image:
    height: int
    width: int
    pixels: List[str]
    infinity_pixel: str = '.'


class Unhandled(Exception):
    pass


def check_image_integrity(image: Image):
    if image.height !=image.width:
        raise Unhandled
    for row in image.pixels:
        if len(row) != image.width:
            raise Unhandled
    if image.infinity_pixel not in ("#", "."):
        raise Unhandled


def get_pixel(image: Image, x: int, y: int) -> str:
    if -1 < x < image.width and -1 < y < image.height:
        return image.pixels[y][x]
    return image.infinity_pixel


def get_algo_index_for_pixel(image: Image, x: int, y: int) -> int:
    bit_str = ""
    for y_index in range(-1, 2):
        for x_index in range(-1, 2):
            bit_str += get_pixel(image, x + x_index, y + y_index)
    return convert_pixels_to_int(bit_str)


def recusive_enhance(image: Image, algo: EnhancementAlgo, iterations: int) -> Image:
    if iterations < 0:
        raise Unhandled
    for i in range(iterations):
        print (f"Enhancement run {i}: {image.width}x{image.height}")
        image = enhance(image, algo)
    return image


def enhance(image: Image, algo: EnhancementAlgo) -> Image:
    enhanced_image = Image(
        infinity_pixel=algo.pixel_map[get_algo_index_for_pixel(image, -100, -100)],
        height=image.height+4,
        width=image.width+4,
        pixels=[]
    )
    for y in range(enhanced_image.height):
        row = ""
        for x in range(enhanced_image.width):
            source_x = x-2
            source_y = y-2
            index = get_algo_index_for_pixel(image, source_x, source_y)
            row += algo.pixel_map[index]
        enhanced_image.pixels.append(row)
    check_image_integrity(image)
    return enhanced_image


def count_lit_pixels(image: Image) -> int:
    if image.infinity_pixel == "#":
        raise Unhandled

    total = 0
    for row in image.pixels:
        for pixel in row:
            if pixel == "#":
                total += 1
    return total




def load_image(path: str) -> Tuple[EnhancementAlgo, Image]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]
    algo = EnhancementAlgo(pixel_map=lines[0])
    pixels = lines[2:]
    image = Image(height=len(pixels),
                  width=len(pixels[0]),
                  infinity_pixel=".",
                  pixels=pixels)

    return algo, image


def convert_pixels_to_int(pixel_str: str) -> int:
    if len(pixel_str) != 9:
        raise Unhandled
    total = 0
    for i in range(9):
        exponent = 2**(8-i)
        if pixel_str[i] == ".":
            bit = 0
        elif pixel_str[i] == "#":
            bit = 1
        else:
            raise Unhandled
        total += exponent * bit
    return total


if __name__ == "__main__":
    def main():
        algo, image = load_image("input/d20.txt")
        twice = recusive_enhance(image, algo, 2)
        print(count_lit_pixels(twice))
        fifty = recusive_enhance(image, algo, 50)
        print(count_lit_pixels(fifty))
    main()
