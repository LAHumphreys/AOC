class Map:
    def __init__(self, map_data):
        self.map_data = map_data
        self.width = len(map_data[0])
        self.height = len(map_data)

    def get_height(self):
        return self.height

    def get_coord(self, x_coordinate, y_coordinate):
        x_coordinate = x_coordinate % self.width
        return self.map_data[y_coordinate][x_coordinate]


def count_trees(inp, delta_x, delta_y):
    map_obj = Map(inp)
    x_coord = 0
    y_coord = 0
    trees = 0
    while x_coord < (map_obj.get_height() - delta_y):
        y_coord += delta_x
        x_coord += delta_y
        coord = map_obj.get_coord(y_coord, x_coord)
        if coord == ".":
            pass
        elif coord == "#":
            trees += 1
        else:
            raise ValueError

    return trees


if __name__ == "__main__":
    def main():
        coords = []
        with open("input/d03.txt", encoding="ascii") as file_handle:
            for lin in file_handle.readlines():
                if lin[-1] == "\n":
                    lin = lin[0:-1]
                coords.append(lin)
        slopes = [
            [1, 1],
            [3, 1],
            [5, 1],
            [7, 1],
            [1, 2]
        ]
        total = 1
        for slop in slopes:
            [x_point, y_point] = slop
            trees = count_trees(coords, x_point, y_point)
            total *= trees
            print("Trees ({0}, {1}): {2} ({3})".format(x_point, y_point, trees, total))
    main()
