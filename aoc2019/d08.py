import re

from tools.file_loader import load_one
from tools.list_ops import count_items_across_groups, split_to_dims


class BadPixel(Exception):
    pass


def render(dims, layers):
    image = []
    for y_coordinate in range(dims[1]):
        row = ""
        for x_coordinate in range(dims[0]):
            layer_index = 0
            pixel = 2
            while pixel == 2 and layer_index < len(layers):
                pixel = int(layers[layer_index][y_coordinate][x_coordinate])
                layer_index += 1

            if pixel == 1:
                row += "#"
            elif pixel == 0:
                row += " "
            else:
                raise BadPixel

        image.append(row)

    return image


if __name__ == "__main__":
    def main():
        code = load_one("input/d08.txt", re.compile("[0-2]+"))
        layers = split_to_dims(code, (25, 6, None))
        min_layer = min(layers, key=lambda layer: count_items_across_groups(layer)["0"])
        pixel_count = count_items_across_groups(min_layer)
        print(pixel_count["1"] * pixel_count["2"])

        for row in render((25, 6), layers):
            print(row)


    main()
