from enum import Enum
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Signal:
    source: str
    target: str
    high: bool


class SwitchType(Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "broadcaster"


class Unimplemented(Exception):
    pass


class Switch:
    def __init__(self, key: str):
        self.id: str = key
        self.clients: list[str] = []

    def register_input(self, key: str):
        pass

    def register_client(self, key: str):
        self.clients += [key]

    def input_pulse(self, source: str, high: bool, output: list[Signal]):
        raise Unimplemented

    def state_string(self):
        return self.id


class SinkSwitch(Switch):
    def __init__(self, key: str):
        super().__init__(key)

    def input_pulse(self, source: str, high: bool, output: list[Signal]):
        pass


@dataclass
class SwitchSet:
    switches: dict[str, Switch]


class FlipFlop(Switch):
    def __init__(self, key: str):
        super().__init__(key)
        self.on: bool = False

    def input_pulse(self, source: str, high: bool, output: list[Signal]):

        if high:
            return
        self.on = not self.on
        for client_key in self.clients:
            high = True if self.on else False
            output += [Signal(source=self.id, high=high, target=client_key)]

    def state_string(self):
        state = super().state_string()
        state += "+" if self.on else "-"
        return state


class Broadcaster(Switch):
    def __init__(self):
        super().__init__("broadcaster")

    def input_pulse(self, source: str, high: bool, output: list[Signal]):
        for client_key in self.clients:
            output += [Signal(source=self.id, high=high, target=client_key)]
        pass


class Conjunction(Switch):
    def __init__(self, key: str):
        super().__init__(key)
        self.state: dict[str, bool] = {}

    def register_input(self, key: str):
        self.state[key] = False
        pass

    def input_pulse(self, source: str, high: bool, output: list[Signal]):
        self.state[source] = high
        for client_key in self.clients:
            high = not all(self.state.values())
            output += [Signal(source=self.id, high=high, target=client_key)]
        pass

    def state_string(self):
        state = super().state_string()
        for key, on in self.state.items():
            state += key + "+" if on else "-"
        return state


def parse_input_line(line: str) -> Switch:
    id_str, clients_str = line.split(" -> ")
    if id_str[0] == "%":
        switch = FlipFlop(id_str[1:].strip())
    elif id_str[0] == "&":
        switch = Conjunction(id_str[1:].strip())
    else:
        switch = Broadcaster()
    for client in clients_str.split(", "):
        switch.register_client(client)
    return switch

@dataclass
class CachedState:
    high: int
    low: int
    switches: SwitchSet


def press_the_button(switches: SwitchSet, count: int) -> int:
    cache: dict[str, CachedState] = {}
    total_high = 0
    total_low = 0
    while count > 0:
        key = get_state_key(switches)
        if key in cache:
            state = cache[key]
            high, low = state.high, state.low
            switches = state.switches
        else:
            high, low = count_pulses(switches)
            cache[key] = CachedState(high=high, low=low, switches=deepcopy(switches))
        total_high += high
        total_low += low
        count -= 1
    return total_high * total_low


def count_pulses(switches: SwitchSet) -> tuple[int, int]:
    pulse_count_low = 0
    pulse_count_high = 0
    instructions: list[Signal] = [Signal(source="button", target="broadcaster", high=False)]
    while instructions:
        signal = instructions.pop(0)
        switch = switches.switches[signal.target]
        switch.input_pulse(signal.source, signal.high, instructions)
        if signal.high:
            pulse_count_high += 1
        else:
            pulse_count_low += 1
    return pulse_count_high, pulse_count_low


def load_switches(file_name: str) -> SwitchSet:
    with open(file_name) as input_file:
        switches = [parse_input_line(line.strip(" \n")) for line in input_file.readlines()]

    switch_map = SwitchSet(switches={switch.id: switch for switch in switches})
    for switch in switches:
        for target in switch.clients:
            if target not in switch_map.switches:
                switch_map.switches[target] = SinkSwitch(target)
            switch_map.switches[target].register_input(switch.id)
    return switch_map


def get_state_key(switches: SwitchSet) -> str:
    return ",".join(switch.state_string() for switch in switches.switches.values())


def main():
    switches = load_switches("input/d20.txt")
    print(press_the_button(switches, 1000))
    pass


if __name__ == "__main__":
    main()
