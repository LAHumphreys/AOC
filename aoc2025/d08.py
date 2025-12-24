from dataclasses import dataclass
import math

debug_on = True

def debug(msg: str):
    if debug_on:
        print(msg)

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.z < other.z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

@dataclass(frozen=True)
class Connection:
    distance: float
    start: Point
    end: Point

def make_connection(a: Point, b: Point) -> Connection:
    start = min(a, b)
    end = max(a, b)
    return Connection(distance=distance(start, end), start=start, end=end)


@dataclass
class ConnectionMap:
    possible_connections: list[Connection]

    def __post_init__(self):
        self.possible_connections.sort(key=lambda c: c.distance)

class Circuit:
    next_id = 0
    def __init__(self, conn: Connection):
        self.id = Circuit.next_id
        Circuit.next_id += 1
        # N is small enough simply forward searching the
        # list is likely good enough
        self.points: list[Point] = [conn.start, conn.end]
        self.connections: list[Connection] = [conn]

    def connection_would_connect(self, conn: Connection) -> bool:
        if conn in self.connections:
            raise ValueError("Connection already exists in circuit")
        return conn.start in self.points or conn.end in self.points

    def add_connection(self, conn: Connection, allow_disconnects: bool = False):
        if conn in self.connections:
            raise ValueError("Connection already exists in circuit")
        points_added = 0
        for point in (conn.start, conn.end):
            if point not in self.points:
                points_added += 1
                self.points.append(point)
        if points_added == 2 and not allow_disconnects:
            raise ValueError("Disconnected circuit")
        self.connections.append(conn)

    def __str__(self) -> str:
        lines = [f"Circuit with {len(self.points)} points and {len(self.connections)} connections:"]
        for conn in self.connections:
            lines.append(f"  {conn.start} <-> {conn.end} (distance: {conn.distance:.2f})")
        return "\n".join(lines)

def make_circuits(conns: list[Connection]) -> list[Circuit]:
    circuits = []
    for i, conn in enumerate(conns):
        debug(f"\nProcessing connection {i+1}/{len(conns)}: {conn.start} <-> {conn.end} ({conn.distance:.2f})")
        connecting_circuits: list[Circuit] = []
        for circuit in circuits:
            if circuit.connection_would_connect(conn):
                connecting_circuits.append(circuit)
        if len(connecting_circuits) > 2:
            raise ValueError("Too many circuits found")
        if len(connecting_circuits) == 2:
            merged_circuit, disabled_circuit = connecting_circuits
            debug(f"  Circuits {merged_circuit.id} and {disabled_circuit.id} both connect and will be merged")
            merged_circuit.add_connection(conn)
            for conn in disabled_circuit.connections:
                merged_circuit.add_connection(conn, allow_disconnects=True)
            circuits.remove(disabled_circuit)
            debug(f"  Merged   circuit {merged_circuit.id} (now {len(merged_circuit.points)} points)")
        elif len(connecting_circuits) == 1:
            circuit = connecting_circuits[0]
            circuit.add_connection(conn)
            debug(f"  Adding to existing circuit {circuit.id} (now {len(circuit.points)} points)")
        else:
            debug(f"  Creating new circuit {len(circuits)}")
            circuits.append(Circuit(conn))

    debug(f"\nFinal circuits: {len(circuits)} total")
    for i, circuit in enumerate(circuits):
        debug(f"  Circuit {i}: {len(circuit.points)} points, {len(circuit.connections)} connections")

    return sorted(circuits, key=lambda c: len(c.points), reverse=True)


def load_sample(file: str) -> list[Point]:
    with open(file, "r", encoding="utf-8") as f:
        points = []
        for x, y, z in (line.strip().split(",") for line in f.readlines()):
            points.append(Point(int(x), int(y), int(z)))
    return points

# We've only got a 1000 points. Do it dumb first, and see if its fast enough
def distance(point_1: Point, point_2: Point) -> float:
    return math.sqrt(
            (point_1.x - point_2.x)**2 +
            (point_1.y - point_2.y)**2 +
            (point_1.z - point_2.z)**2)


# We've only got a 1000 points. Do it dumb first, and see if its fast enough
def find_nearest(point: Point, points: list[Point]) -> Point:
    other_points = (x for x in points if x != point)
    return min(other_points, key=lambda p: distance(point, p))

def map_points(points: list[Point]) -> ConnectionMap:
    connections = []

    for point_idx in range(len(points)):
        for other_idx in range(point_idx+1, len(points)):
            conn = make_connection(points[point_idx], points[other_idx])
            connections.append(conn)

    return ConnectionMap(possible_connections=connections)


def part1(data: list[Point], num_connections: int) -> int:
    conn_map = map_points(data)
    circuits = make_circuits(conn_map.possible_connections[:num_connections])
    return len(circuits[0].points) * len(circuits[1].points) * len(circuits[2].points)


def part2(data: list[Point]) -> int:
    return len(data)


def main():
    try:
        data = load_sample("input/d08.txt")
        print(f"Part 1: {part1(data, 1000)}")
        print(f"Part 2: {part2(data)}")
    except FileNotFoundError:
        print("Input file not found.")


if __name__ == "__main__":
    main()
