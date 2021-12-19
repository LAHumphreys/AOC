from unittest import TestCase

from aoc2021.d19 import load_readouts, Point, ScannerReadout, create_reference_frame
from aoc2021.d19 import Frame, apply_reference_frame, find_aligned_frames, find_reference_frame
from aoc2021.d19 import orientation_set, reorient_to_default, Orientation, realign_scanner
from aoc2021.d19 import find_unique_points, get_greatest_distance
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Parser(TestCase):
    def test_load_scanners(self):
        readouts = load_readouts(get_test_file_path("samples/d19/tiny.txt"))
        self.assertEqual(len(readouts), 2)
        scanner_0 = ScannerReadout(
            beacons=[Point(0,2,0), Point(4,1,0), Point(3,3,0)],
            name="--- scanner 0 ---")
        scanner_1 = ScannerReadout(
            beacons=[Point(-1,-1,0), Point(-5,0,0), Point(-2,1,0)],
            name="--- scanner 1 ---")
        self.assertListEqual(readouts, [scanner_0, scanner_1])


class SimpleAlignment(TestCase):
    def test_tiny_example(self):
        readouts = load_readouts(get_test_file_path("samples/d19/tiny.txt"))
        lhs_frame, rhs_frame, orientation = find_aligned_frames(readouts[0], readouts[1], 3)
        lhs_beacons = [apply_reference_frame(beacon, lhs_frame) for beacon in readouts[0].beacons]
        rhs_beacons = [apply_reference_frame(beacon, rhs_frame) for beacon in readouts[1].beacons]
        lhs_beacons.sort()
        rhs_beacons.sort()
        self.assertListEqual(lhs_beacons, rhs_beacons)

    def find_and_apply_common_frame(self, lhs: ScannerReadout, rhs: ScannerReadout, threshold: int):
        rhs_frame, rhs_orientation = find_reference_frame(lhs, rhs, threshold)
        aligned_beacons = reorient_to_default(rhs.beacons, rhs_orientation)
        rhs_beacons = [apply_reference_frame(beacon, rhs_frame) for beacon in aligned_beacons]
        rhs_beacons.sort()
        lhs.beacons.sort()
        self.assertListEqual(lhs.beacons, rhs_beacons)

    def test_tiny_example_ref_frame(self):
        readouts = load_readouts(get_test_file_path("samples/d19/tiny.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 3)

    def test_small_no_rotation(self):
        readouts = load_readouts(get_test_file_path("samples/d19/small/no_rotation.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 5)

    def test_small_first_rotation(self):
        readouts = load_readouts(get_test_file_path("samples/d19/small/roation_1.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 5)

    def test_small_second_rotation(self):
        readouts = load_readouts(get_test_file_path("samples/d19/small/roation_2.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 5)

    def test_small_third_rotation(self):
        readouts = load_readouts(get_test_file_path("samples/d19/small/roation_3.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 5)

    def test_small_fourth_rotation(self):
        readouts = load_readouts(get_test_file_path("samples/d19/small/roation_4.txt"))
        self.find_and_apply_common_frame(readouts[0], readouts[1], 5)

    def test_overlapping_sample_pair(self):
        readouts = load_readouts(get_test_file_path("samples/d19/overlapping.txt"))
        rhs_frame, rhs_orientation = find_reference_frame(readouts[0], readouts[1], 12)
        rhs_aligned = realign_scanner(readouts[1], rhs_orientation)
        rhs_beacons = [apply_reference_frame(beacon, rhs_frame) for beacon in rhs_aligned.beacons]
        lhs_beacons = {beacon for beacon in readouts[0].beacons}
        common_beacons = {beacon for beacon in rhs_beacons if beacon in lhs_beacons}
        expected_beacons = {
            Point(x=-618, y=-824, z=-621),
            Point(x=-537, y=-823, z=-458),
            Point(x=-447, y=-329, z=318),
            Point(x=404, y=-588, z=-901),
            Point(x=544, y=-627, z=-890),
            Point(x=528, y=-643, z=409),
            Point(x=-661, y=-816, z=-575),
            Point(x=390, y=-675, z=-793),
            Point(x=423, y=-701, z=434),
            Point(x=-345, y=-311, z=381),
            Point(x=459, y=-707, z=401),
            Point(x=-485, y=-357, z=347)
        }
        self.assertSetEqual(common_beacons, expected_beacons)

    def test_overlapping_pair_chain(self):
        expected_beacons = {
            Point(x=459, y=-707, z=401),
            Point(x=-739, y=-1745, z=668),
            Point(x=-485, y=-357, z=347),
            Point(x=432, y=-2009, z=850),
            Point(x=528, y=-643, z=409),
            Point(x=423, y=-701, z=434),
            Point(x=-345, y=-311, z=381),
            Point(x=408, y=-1815, z=803),
            Point(x=534, y=-1912, z=768),
            Point(x=-687, y=-1600, z=576),
            Point(x=-447, y=-329, z=318),
            Point(x=-635, y=-1737, z=486),
        }
        readouts = load_readouts(get_test_file_path("samples/d19/overlapping.txt"))
        reference_scanner = readouts[0]
        mid_scanner = readouts[1]
        end_scanner = readouts[4]
        self.assertEqual(reference_scanner.name, "--- scanner 0 ---")
        self.assertEqual(mid_scanner.name, "--- scanner 1 ---")
        self.assertEqual(end_scanner.name, "--- scanner 4 ---")
        mid_frame, mid_orientation = find_reference_frame(reference_scanner, mid_scanner, 12)
        mid_aligned = realign_scanner(mid_scanner, mid_orientation)
        mid_beacons = {apply_reference_frame(beacon, mid_frame) for beacon in mid_aligned.beacons}

        end_frame, end_orientation = find_reference_frame(mid_aligned, end_scanner, 12)
        end_aligned = realign_scanner(end_scanner, end_orientation)
        end_beacons = [apply_reference_frame(beacon, end_frame) for beacon in end_aligned.beacons]
        end_beacons = [apply_reference_frame(beacon, mid_frame) for beacon in end_beacons]

        common_beacons = {beacon for beacon in end_beacons if beacon in mid_beacons}
        self.assertSetEqual(common_beacons, expected_beacons)


class FindCommonBeacons(TestCase):
    def test_pair(self):
        readouts = load_readouts(get_test_file_path("samples/d19/overlapping.txt"))
        scanners = [readouts[0], readouts[1]]
        unique_beacons = find_unique_points(scanners)[0]
        common_beacons = {
            Point(x=-618, y=-824, z=-621),
            Point(x=-537, y=-823, z=-458),
            Point(x=-447, y=-329, z=318),
            Point(x=404, y=-588, z=-901),
            Point(x=544, y=-627, z=-890),
            Point(x=528, y=-643, z=409),
            Point(x=-661, y=-816, z=-575),
            Point(x=390, y=-675, z=-793),
            Point(x=423, y=-701, z=434),
            Point(x=-345, y=-311, z=381),
            Point(x=459, y=-707, z=401),
            Point(x=-485, y=-357, z=347)
        }
        expected_beacons_count = len(readouts[0].beacons) + len(readouts[1].beacons) - len(common_beacons)
        self.assertEqual(len(unique_beacons), expected_beacons_count)

    def test_all_beacons(self):
        readouts = load_readouts(get_test_file_path("samples/d19/overlapping.txt"))
        scanners = readouts
        unique_beacons, frames = find_unique_points(scanners)
        self.assertEqual(len(unique_beacons), 79)
        self.assertEqual(get_greatest_distance([frame for _, frame in frames.items()]), 3621)


class Rotations(TestCase):
    def find_common_rotation(self, lhs: ScannerReadout, rhs: ScannerReadout):
        final_orientation: Orientation = None
        for orientation in orientation_set():
            rhs_aligned = reorient_to_default(rhs.beacons, orientation)
            aligned = True
            for beacon in rhs_aligned:
                if beacon not in lhs.beacons:
                    aligned = False
            if aligned:
                final_orientation = orientation
                break
        rhs_aligned = reorient_to_default(rhs.beacons, final_orientation)
        rhs_aligned.sort()
        lhs.beacons.sort()
        self.assertListEqual(lhs.beacons, rhs_aligned)


    def test_default(self):
        readouts = load_readouts(get_test_file_path("samples/d19/rotations/default.txt"))
        self.find_common_rotation(readouts[0], readouts[1])

    def test_sample_one(self):
        readouts = load_readouts(get_test_file_path("samples/d19/rotations/sample1.txt"))
        self.find_common_rotation(readouts[0], readouts[1])

    def test_sample_two(self):
        readouts = load_readouts(get_test_file_path("samples/d19/rotations/sample2.txt"))
        self.find_common_rotation(readouts[0], readouts[1])

    def test_sample_three(self):
        readouts = load_readouts(get_test_file_path("samples/d19/rotations/sample3.txt"))
        self.find_common_rotation(readouts[0], readouts[1])

    def test_sample_four(self):
        readouts = load_readouts(get_test_file_path("samples/d19/rotations/sample4.txt"))
        self.find_common_rotation(readouts[0], readouts[1])

class Frames(TestCase):
    zero_point: Point = Point(x=0, y=0, z=0)

    def test_ref_frame(self):
        ref_point = Point(x=1,y=2,z=3)
        frame = create_reference_frame(ref_point)
        self.assertEqual(frame, Frame(x=-1, y=-2, z=-3))
        self.assertEqual(apply_reference_frame(ref_point, frame), self.zero_point)
        self.assertEqual(apply_reference_frame(ref_point, frame), self.zero_point)
