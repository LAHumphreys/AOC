class Map:
    def __init__(self, map_data):
        self.map_data = map_data
        self.width = len(map_data[0])
        self.height = len(map_data)

    def get_height(self):
        return self.height

    def get_coord(self, x, y):
        x = x % self.width
        return self.map_data[y][x]


def count_trees(inp, dx, dy):
    map_obj = Map(inp)
    y = 0
    x = 0
    trees = 0
    while y < (map_obj.get_height() - dy):
        x += dx
        y += dy
        coord = map_obj.get_coord(x, y)
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
        f = open("input/d03.txt")
        for lin in f.readlines():
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
            [x, y] = slop
            trees = count_trees(coords, x, y)
            total *= trees
            print("Trees ({0}, {1}): {2} ({3})".format(x, y, trees, total))
        main()
