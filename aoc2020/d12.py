from tools.paths import make_path, rotate, TurnDirection
from tools.paths import make_path_from_vectors, CardinalPoint, Point, PathPoint


def convert_to_std(advent_format):
    tools_format = []
    conversion = {
        "N": "U",
        "S": "D",
        "E": "R",
        "W": "L",
        "L": "A",
        "R": "C",
        "F": "F"
    }
    for instruction in advent_format:
        letter = instruction[0]
        tools_format.append(conversion[letter] + instruction[1:])
    return tools_format


def load_direction(path):
    with open(path, encoding="ascii") as file:
        return convert_to_std(line for line in file.read().split("\n"))


def make_ship_path(directions):
    return make_path_from_vectors(directions, CardinalPoint.EAST)


def move_by_waypoint(directions):
    way_point = PathPoint(10, 1, 0)
    ship = Point(0, 0)
    for direction in directions:
        code = direction[0]
        argument = int(direction[1:])
        if code == "F":
            ship_x = ship.x_coordinate + argument * way_point.get_point().x_coordinate
            ship_y = ship.y_coordinate + argument * way_point.get_point().y_coordinate
            ship = Point(ship_x, ship_y)
        elif code in ("C", "A"):
            if code == "C":
                turn = TurnDirection.RIGHT
            else:
                turn = TurnDirection.LEFT
            new_way_point = rotate(Point(0, 0), way_point.get_point(), turn, argument)
            way_point = PathPoint(new_way_point.x_coordinate, new_way_point.y_coordinate, 0)
        else:
            way_path = make_path(way_point, direction)
            way_point = way_path[-1]

    return ship


if __name__ == "__main__":
    def main():
        directions = load_direction("input/d12.txt")
        path = make_ship_path(directions)
        print(path[-1].get_point().manhattan_distance())
        final_destination = move_by_waypoint(directions)
        print(final_destination)
        print(final_destination.manhattan_distance())


    main()
