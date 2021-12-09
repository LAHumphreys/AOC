from dataclasses import dataclass
from typing import List, Dict
import re
from tools.file_loader import load_patterns

length_ref_data: Dict[int, List[int]] = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}


@dataclass
class SignalSet:
    signals: List[str]
    display: List[str]


def map_signals(signals: List[str]) -> Dict[str, int]:
    signals = ["".join(sorted(signal)) for signal in signals]

    signal_map: Dict[str, int] = {}
    for signal in signals:
        options = length_ref_data[len(signal)]
        if len(options) == 1:
            signal_map[signal] = options[0]

    for signal in signals:
        signal_count = {digit: 0 for _, digit in signal_map.items()}
        for line in signal:
            for digit_signal, digit in signal_map.items():
                if line in digit_signal:
                    signal_count[digit] += 1
        if len(signal) == 5 and signal_count[1] == 2:
            signal_map[signal] = 3
        elif len(signal) == 5 and signal_count[4] == 3:
            signal_map[signal] = 5
        elif len(signal) == 5 and signal_count[4] == 2:
            signal_map[signal] = 2
        elif len(signal) == 6 and signal_count[4] == 4:
            signal_map[signal] = 9
        elif len(signal) == 6 and signal_count[7] == 3:
            signal_map[signal] = 0
        elif len(signal) == 6 and signal_count[4] == 3 and signal_count[7] == 2:
            signal_map[signal] = 6

    return signal_map


def load_signal_sets(path: str) -> List[SignalSet]:
    split_regex = re.compile('^([a-g ]+)\\| ([a-z ]+)$')
    signals = [
        SignalSet(signals=signals.split(),
                  display=display.split()) for signals, display in load_patterns(split_regex, path)]
    return signals


def get_value(signal: SignalSet) -> int:
    signal_map = map_signals(signal.signals)
    display = ["".join(sorted(digit)) for digit in signal.display]
    value = 1000 * signal_map[display[0]]
    value += 100 * signal_map[display[1]]
    value += 10 * signal_map[display[2]]
    value += signal_map[display[3]]
    return value


def part_two(signals: List[SignalSet]) -> int:
    return sum(map(get_value, signals))


def part_one(signals: List[SignalSet]) -> int:
    count = 0
    for signal in signals:
        signal_map = map_signals(signal.signals)
        for digit in signal.display:
            digit = "".join(sorted(digit))
            value = signal_map.get(digit, -1)
            if value in (1, 4, 7, 8):
                count += 1

    return count


if __name__ == "__main__":
    def main():
        signals = load_signal_sets("input/d08.txt")
        print(part_one(signals))
        print(part_two(signals))
    main()
