from dataclasses import dataclass
from typing import Callable, List, Tuple, Set, Dict


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return self.x + 900000*self.y + 90000*90000*self.z

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        elif self.y != other.y:
            return self.y < other.y
        elif self.z != other.z:
            return self.z < other.z
        else:
            return False


Orientation = Callable[[Point], Point]


def default_orientation(point: Point) -> Point:
    return point


def orientation_set():
    # TODO technically we're producing twice as many as necessary here
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                yield lambda p: Point(x=x*p.x, y=y*p.y, z=z*p.z)
                yield lambda p: Point(x=x*p.x, y=y*p.z, z=z*p.y)

                yield lambda p: Point(x=x*p.y, y=y*p.x, z=z*p.z)
                yield lambda p: Point(x=x*p.y, y=y*p.z, z=z*p.x)

                yield lambda p: Point(x=x*p.z, y=y*p.y, z=z*p.x)
                yield lambda p: Point(x=x*p.z, y=y*p.x, z=z*p.y)


@dataclass
class Frame(Point):
    pass


@dataclass
class ScannerReadout:
    name: str
    beacons: List[Point]


def reorient_to_default(beacons: List[Point], orientation: Orientation) -> List[Point]:
    return [orientation(beacon) for beacon in beacons]


def realign_scanner(scanner: ScannerReadout, orientation: Orientation) -> ScannerReadout:
    return ScannerReadout(name=scanner.name, beacons=reorient_to_default(scanner.beacons, orientation))


def load_readouts(path: str) -> List[ScannerReadout]:
    readouts = []
    readout = []
    name = ""
    with open(path, encoding="ascii") as file:
        for line in file.readlines():
            if line[0:3] == "---":
                if readout:
                    readouts.append(ScannerReadout(name=name, beacons=readout))
                readout = []
                name = line.replace("\n", "")
            elif len(line) < 5:
                pass
            else:
                x, y, z = (int(point) for point in line.replace("\n", "").split(","))
                readout.append(Point(x=x, y=y, z=z))
    if readout:
        readouts.append(ScannerReadout(name=name, beacons=readout))
    return readouts


class Unalignable(Exception):
    pass


def create_reference_frame(beacon: Point) -> Frame:
    return Frame(x=-1*beacon.x, y=-1*beacon.y, z=-1*beacon.z)


def apply_reference_frame(beacon: Point, frame: Frame) -> Point:
    return Point(x=beacon.x+frame.x,
                 y=beacon.y+frame.y,
                 z=beacon.z+frame.z)


def apply_reference_frame_to_frame(reference: Frame, frame: Frame) -> Frame:
    return Frame(x=frame.x - reference.x,
                 y=frame.y - reference.y,
                 z=frame.z - reference.z)


def chain_frames(reference: Frame, frame: Frame) -> Frame:
    return Frame(x=frame.x + reference.x,
                 y=frame.y + reference.y,
                 z=frame.z + reference.z)


def find_unique_points(scanners: List[ScannerReadout]) -> Tuple[Set[Point], Dict[str, Frame]]:
    aligned_scanners = [scanners[0]]
    ref_frames = {
        scanners[0].name: Frame(x=0, y=0, z=0)
    }

    to_align = scanners[1:]
    while to_align:
        print("Aligned {0} of {1} scanners".format(len(aligned_scanners), len(scanners)))
        unaligned_beacons = []
        for working_scanner in to_align:
            print("Attempting to align: " + working_scanner.name)
            aligned = False
            for ref_scanner in aligned_scanners:
                try:
                    working_frame, working_orientation = find_reference_frame(ref_scanner, working_scanner, 12)
                    aligned_scanners.append(realign_scanner(working_scanner, working_orientation))
                    ref_frames[working_scanner.name] =\
                        chain_frames(ref_frames[ref_scanner.name], working_frame)
                    aligned = True
                    break
                except Unalignable:
                    pass
            if not aligned:
                unaligned_beacons.append(working_scanner)
        to_align = unaligned_beacons

    if len(aligned_scanners) != len(scanners):
        raise Unhandled

    ref_scanner = aligned_scanners[0]
    unique_points = {beacon for beacon in ref_scanner.beacons}
    for working_scanner in aligned_scanners[1:]:
        frame = ref_frames[working_scanner.name]
        working_beacons = [apply_reference_frame(beacon, frame) for beacon in working_scanner.beacons]
        for beacon in working_beacons:
            unique_points.add(beacon)
    return unique_points, ref_frames


def find_aligned_frames(lhs: ScannerReadout, rhs: ScannerReadout, threshold: int) -> Tuple[Frame, Frame, Orientation]:
    """
    We want to find a frame where the beacons settle into the same coordinates. Fortunately we know that
    both readouts have a number of shared points so there are a fixed # of frames we can inspect.

    Since there are multiple common Beacons, there are multiple valid answers here - there is no
    "best", we just want one that works
    """
    for lhs_beacon in lhs.beacons:
        lhs_frame = create_reference_frame(lhs_beacon)
        lhs_beacons_in_frame = {apply_reference_frame(beacon, lhs_frame) for beacon in lhs.beacons}
        for orientation in orientation_set():
            aligned_beacons = reorient_to_default(rhs.beacons, orientation)
            for rhs_beacon in aligned_beacons:
                rhs_frame = create_reference_frame(rhs_beacon)
                matches = 0
                for beacon in aligned_beacons:
                    if apply_reference_frame(beacon, rhs_frame) in lhs_beacons_in_frame:
                        matches += 1
                    if matches >= threshold:
                        return lhs_frame, rhs_frame, orientation

    raise Unalignable


def find_reference_frame(reference: ScannerReadout, other: ScannerReadout, threshold: int) -> Tuple[Frame, Orientation]:
    ref_frame, other_frame, orientation = find_aligned_frames(reference, other, threshold)
    #
    # But we don't want to transpose both of them, we want to force everything into
    # the reference Scanner's p.o.v
    #
    return apply_reference_frame_to_frame(ref_frame, other_frame), orientation


class Unhandled(Exception):
    pass


def get_greatest_distance(frames: List[Frame]) -> int:
    greatest = 0
    for frame in frames:
        for other_frame in frames:
            distance = abs(frame.x - other_frame.x) + abs(frame.y - other_frame.y) + abs(frame.z - other_frame.z)
            if distance > greatest:
                greatest = distance
    return greatest


if __name__ == "__main__":
    def main():
        scanners = load_readouts("input/d19.txt")
        unique_beacons, frames = find_unique_points(scanners)
        print(len(unique_beacons))
        print(get_greatest_distance([frame for _, frame in frames.items()]))
        pass
    main()
