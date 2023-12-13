from unittest import TestCase

from aoc2023.d20 import FlipFlop, Signal, load_switches, count_pulses
from aoc2023.d20 import Conjunction, parse_input_line, Broadcaster, press_the_button
from tests.aoc2023Tests.aoc2023_common import get_test_file_path


class TestFlipFlop(TestCase):
    def setUp(self):
        self.signals: list[Signal] = []

    def test_initial_state(self):
        flip_flop = FlipFlop("a")
        self.assertEqual(flip_flop.id, "a")
        self.assertEqual(flip_flop.on, False)
        self.assertListEqual(self.signals, [])

    def test_high_ignored(self):
        flip_flop = FlipFlop("a")
        flip_flop.input_pulse("source", True, self.signals)
        flip_flop.register_client("b")
        self.assertEqual(flip_flop.id, "a")
        self.assertEqual(flip_flop.on, False)
        self.assertListEqual(self.signals, [])

    def test_high_ignored_still_on(self):
        flip_flop = FlipFlop("a")
        flip_flop.register_client("b")
        flip_flop.on = True
        flip_flop.input_pulse("source", True, self.signals)
        self.assertEqual(flip_flop.id, "a")
        self.assertEqual(flip_flop.on, True)
        self.assertListEqual(self.signals, [])

    def test_low_no_client(self):
        flip_flop = FlipFlop("a")
        flip_flop.input_pulse("source", False, self.signals)
        self.assertEqual(flip_flop.on, True)
        flip_flop.input_pulse("source", False, self.signals)
        self.assertEqual(flip_flop.on, False)
        self.assertListEqual(self.signals, [])

    def test_low_clients(self):
        flip_flop = FlipFlop("a")
        flip_flop.register_client("b")
        flip_flop.register_client("c")
        expected = []
        flip_flop.input_pulse("source", False, self.signals)
        expected += [Signal(source="a", high=True, target="b"), Signal(source="a", high=True, target="c")]
        self.assertEqual(flip_flop.on, True)
        self.assertListEqual(self.signals, expected)
        flip_flop.input_pulse("source", False, self.signals)
        self.assertEqual(flip_flop.on, False)
        expected += [Signal(source="a", high=False, target="b"), Signal(source="a", high=False, target="c")]
        self.assertListEqual(self.signals, expected)


class TestConjunction(TestCase):
    def setUp(self):
        self.signals: list[Signal] = []

    def test_single_client(self):
        switch = Conjunction("con")
        switch.register_input("b")
        switch.register_client("a")
        expected = []
        switch.input_pulse("b", True, self.signals)
        expected += [Signal(source="con", high=False, target="a")]
        self.assertListEqual(self.signals, expected)
        switch.input_pulse("b", True, self.signals)
        expected += [Signal(source="con", high=False, target="a")]
        self.assertListEqual(self.signals, expected)
        switch.input_pulse("b", False, self.signals)
        expected += [Signal(source="con", high=True, target="a")]
        self.assertListEqual(self.signals, expected)

    def test_duel_client(self):
        switch = Conjunction("con")
        switch.register_input("b")
        switch.register_input("c")
        switch.register_client("a")
        expected = []
        switch.input_pulse("b", True, self.signals)
        expected += [Signal(source="con", high=True, target="a")]
        self.assertListEqual(self.signals, expected)
        switch.input_pulse("c", True, self.signals)
        expected += [Signal(source="con", high=False, target="a")]
        self.assertListEqual(self.signals, expected)
        switch.input_pulse("b", False, self.signals)
        expected += [Signal(source="con", high=True, target="a")]
        self.assertListEqual(self.signals, expected)


class TestLoader(TestCase):
    def test_load_broadcaster(self):
        switch = parse_input_line("broadcaster -> a, b, c")
        self.assertEqual(switch.id, "broadcaster")
        self.assertIsInstance(switch, Broadcaster)
        self.assertListEqual(switch.clients, ["a", "b", "c"])

    def test_load_flipflop(self):
        switch = parse_input_line("%b -> c")
        self.assertEqual(switch.id, "b")
        self.assertIsInstance(switch, FlipFlop)
        self.assertListEqual(switch.clients, ["c"])

    def test_load_conjunction(self):
        switch = parse_input_line("&inv -> a")
        self.assertEqual(switch.id, "inv")
        self.assertIsInstance(switch, Conjunction)
        self.assertListEqual(switch.clients, ["a"])

    def test_load_sample_one(self):
        switches = load_switches(get_test_file_path("samples/d20/simple.txt")).switches
        self.assertEqual(switches["broadcaster"].clients, "a  b c".split())
        self.assertIsInstance(switches["broadcaster"], Broadcaster)
        self.assertEqual(switches["a"].clients, ["b"])
        self.assertIsInstance(switches["a"], FlipFlop)
        self.assertEqual(switches["inv"].clients, ["a"])
        self.assertIsInstance(switches["inv"], Conjunction)
        inv: Conjunction = switches["inv"]
        self.assertEqual(inv.state, {"c": False})


class TestCountPulses(TestCase):
    def test_sample_one(self):
        switches = load_switches(get_test_file_path("samples/d20/simple.txt"))
        self.assertEqual(count_pulses(switches), (4, 8))

    def test_buttons_one(self):
        switches = load_switches(get_test_file_path("samples/d20/simple.txt"))
        self.assertEqual(press_the_button(switches, 1000), 32000000)

    def test_buttons_two(self):
        switches = load_switches(get_test_file_path("samples/d20/second_eg"))
        self.assertEqual(press_the_button(switches, 1000), 11687500)

