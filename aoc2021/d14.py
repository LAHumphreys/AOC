from typing import Dict


def load_map(path: str) -> Dict[str, str]:
    with open(path, encoding="ascii") as file:
        lines = [line.replace("\n", "").split(" -> ") for line in file.readlines()]
    return dict(lines)


def encode_poly(poly: str) -> Dict[str, int]:
    encoding = {}
    for i in range(len(poly)-1):
        pair = poly[i:i+2]
        encoding.setdefault(pair, 0)
        encoding[pair] += 1

    end = poly[-1] + "\n"
    encoding[end] = 1
    return encoding


def apply_expansions(expansions: Dict[str, str], poly: str) -> str:
    output = poly[0]
    for i in range(len(poly)-1):
        expansion = expansions.get(poly[i:i+2])
        output += expansion + poly[i+1]
    return output


def expand_encoded(expansions: Dict[str, str], poly: Dict[str, int]) -> Dict[str, int]:
    expanded_poly = {}
    for pair, count in poly.items():
        if pair in expansions:
            expansion = expansions[pair]
            pairs = [pair[0] + expansion, expansion + pair[1]]
        else:
            pairs = [pair]

        for new_pair in pairs:
            expanded_poly.setdefault(new_pair, 0)
            expanded_poly[new_pair] += count

    return expanded_poly


def apply_steps(steps: int, expansions: Dict[str, str], poly: str) -> str:
    for _ in range(steps):
        poly = apply_expansions(expansions, poly)
    return poly


def score_steps(steps: int, expansions: Dict[str, str], poly: str) -> int:
    encoded = encode_poly(poly)
    for _ in range(steps):
        encoded = expand_encoded(expansions, encoded)
    return get_encoded_score(encoded)


def get_score(poly: str) -> int:
    count: Dict[str, int] = {}
    for char in poly:
        count.setdefault(char, 0)
        count[char] += 1

    counts = list(count.values())
    counts.sort()
    return counts[-1] - counts[0]


def get_encoded_score(poly: Dict[str, int]) -> int:
    count: Dict[str, int] = {}
    for pair, pair_count in poly.items():
        count.setdefault(pair[0], 0)
        count[pair[0]] += pair_count

    counts = list(count.values())
    counts.sort()
    return counts[-1] - counts[0]


if __name__ == "__main__":
    def main():
        start_poly = "FPNFCVSNNFSFHHOCNBOB"
        expansions = load_map("input/d14.txt")
        print(get_score(apply_steps(10, expansions, start_poly)))
        print(score_steps(10, expansions, start_poly))
        print(score_steps(40, expansions, start_poly))

    main()
