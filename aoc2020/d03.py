class Map:
    def __init__(self, map):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)

    def GetHeight(self):
        return self.height

    def GetCoord(self, x, y):
        x = x % self.width
        return self.map[y][x]

def countTrees(input, dx, dy):
    map = Map(input)
    y = 0
    x = 0
    trees = 0
    while y < (map.GetHeight()-dy):
        x += dx
        y += dy
        coord = map.GetCoord(x,y)
        if coord == ".":
            pass
        elif coord == "#":
            trees +=1
        else:
            raise ValueError

    return trees

if __name__ == "__main__":
    coords = []
    f = open ("input/d03.txt")
    for l in f.readlines():
        if l[-1] == "\n":
            l = l[0:-1]
        coords.append(l)
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
        trees = countTrees(coords, x, y)
        total *= trees
        print ("Trees ({0}, {1}): {2} ({3})".format(x, y, trees, total))
