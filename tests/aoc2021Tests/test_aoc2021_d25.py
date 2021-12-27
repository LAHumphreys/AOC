from unittest import TestCase

from aoc2021.d25 import load_seabed, do_step, Seabed, step_until_stop
from tests.aoc2021Tests.aoc2021_common import get_test_file_path


class Loader(TestCase):
    def test_initial(self):
        seabed = load_seabed(get_test_file_path("samples/d25/small/initial.txt"))
        self.assertEqual(seabed.height, 7)
        self.assertEqual(seabed.width, 7)
        self.assertListEqual(seabed.seabed, [
            "...>...",
            ".......",
            "......>",
            "v.....>",
            "......>",
            ".......",
            "..vvv.."
        ])


class Stepper(TestCase):
    def test_step_east(self):
        start_bed = Seabed(height=2, width=2, seabed=[">.", ".>"])
        expected_bed = Seabed(height=2, width=2, seabed=[".>", ">."])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_step_east_blocked(self):
        start_bed = Seabed(height=2, width=2, seabed=[">v", ".>"])
        expected_bed = Seabed(height=2, width=2, seabed=[">.", ">v"])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_step_east_wrapblocked(self):
        start_bed = Seabed(height=2, width=2, seabed=["v>", ".."])
        expected_bed = Seabed(height=2, width=2, seabed=[".>", "v."])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_step_south(self):
        start_bed = Seabed(height=2, width=2, seabed=["v.", ".v"])
        expected_bed = Seabed(height=2, width=2, seabed=[".v", "v."])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_step_south_blocked(self):
        start_bed = Seabed(height=2, width=2, seabed=[">.", ".v"])
        expected_bed = Seabed(height=2, width=2, seabed=[".>", ".v"])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_wide_block(self):
        start_bed = Seabed(height=2, width=7, seabed=["v.....>", "......."])
        expected_bed = Seabed(height=2, width=7, seabed=["......>", "v......"])
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_small_step(self):
        start_bed = load_seabed(get_test_file_path("samples/d25/small/initial.txt"))
        expected_step = load_seabed(get_test_file_path("samples/d25/small/step1.txt"))
        stepped = do_step(start_bed)
        self.assertEqual(expected_step, stepped)

    def test_small_steps(self):
        start_bed = load_seabed(get_test_file_path("samples/d25/small/initial.txt"))
        expected_step = load_seabed(get_test_file_path("samples/d25/small/step4.txt"))
        stepped = do_step(do_step(do_step(do_step(start_bed))))
        self.assertEqual(expected_step, stepped)

    def test_stop_step(self):
        start_bed = load_seabed(get_test_file_path("samples/d25/stop/initial.txt"))
        expected_bed = load_seabed(get_test_file_path("samples/d25/stop/step1.txt"))
        stepped = do_step(start_bed)
        self.assertEqual(expected_bed, stepped)

    def test_stopper_steps(self):
        start_bed = load_seabed(get_test_file_path("samples/d25/stop/initial.txt"))
        expected_steps = {
            1: load_seabed(get_test_file_path("samples/d25/stop/step1.txt")),
            10: load_seabed(get_test_file_path("samples/d25/stop/step10.txt")),
        }
        stepped = start_bed
        for i in range (10):
            stepped = do_step(start_bed)
            if i in expected_steps:
                print (i)
                self.assertEqual(expected_steps[i], stepped)

class Stopper(TestCase):
    def test_stop_sample(self):
        start_bed = load_seabed(get_test_file_path("samples/d25/stop/initial.txt"))
        steps, _ = step_until_stop(start_bed)
        self.assertEqual(steps, 58)

