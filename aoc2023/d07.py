from dataclasses import dataclass
from typing import Self
from enum import Enum

CARDS = ["A", "K", "Q", "J", "T"] + [f"{x}" for x in range(9, 1, -1)]
PRIORITY = {card: idx for idx, card in enumerate(CARDS)}


class HandType(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


@dataclass
class Hand:
    hand_str: str
    priority_string: list[int]
    type: HandType
    bid: int

    def __lt__(self, other: Self) -> bool:
        return compare_hands(self, other) == -1


def compare_hands(lhs: Hand, rhs: Hand) -> int:
    if lhs.type.value == rhs.type.value:
        i = 0
        while i < 5 and lhs.priority_string[i] == rhs.priority_string[i]:
            i += 1
        if i == 5:
            return 0
        elif lhs.priority_string[i] > rhs.priority_string[i]:
            return -1
        else:
            return 1
    elif lhs.type.value > rhs.type.value:
        return -1
    else:
        return 1


def load_hands(file_name: str) -> list[Hand]:
    hands: list[Hand] = []
    with open(file_name) as input_file:
        for hand_str, bid in [ln.replace("\n", "").split() for ln in input_file.readlines()]:
            hands.append(Hand(
                hand_str=hand_str,
                priority_string=[PRIORITY[c] for c in hand_str],
                bid=int(bid),
                type=get_hand_type(hand_str)
            ))
    return hands


def count_hand(hand: str) -> dict[str, int]:
    count: dict[str, int] = {}
    for card in hand:
        if card not in count:
            count[card] = 1
        else:
            count[card] += 1
    return count


def get_joker_hand_type(hand: str) -> HandType:
    non_jokers = "".join([c for c in hand if c != "J"])
    if len(non_jokers) != 5:
        if non_jokers == "":
            new_card = "A"
        else:
            count = count_hand(non_jokers)
            max_count = max(count.values())
            # meh, hack it - dinner time
            new_card = None
            for card, card_count in count.items():
                if max_count == card_count:
                    if not new_card:
                        new_card = card
                    elif PRIORITY[card] < PRIORITY[new_card]:
                        new_card = card
        non_jokers += new_card*(5-len(non_jokers))
        return get_hand_type(non_jokers)
    else:
        return get_hand_type(hand)


def convert_jokers(hand: Hand) -> Hand:
    priority = []
    for p in hand.priority_string:
        if p == PRIORITY["J"]:
            priority += [99]
        else:
            priority += [p]
    return Hand(
        bid=hand.bid,
        hand_str=hand.hand_str,
        priority_string=priority,
        type=get_joker_hand_type(hand.hand_str))


def get_hand_type(hand: str) -> HandType:
    count = count_hand(hand)
    max_count = max(count.values())

    if max_count == 5:
        return HandType.FIVE_OF_A_KIND
    elif max_count == 4:
        return HandType.FOUR_OF_A_KIND
    elif max_count == 3:
        if len(count.values()) == 3:
            return HandType.THREE_OF_A_KIND
        else:
            return HandType.FULL_HOUSE
    elif max_count == 2:
        if len(count.values()) == 3:
            return HandType.TWO_PAIR
        else:
            return HandType.ONE_PAIR

    return HandType.HIGH_CARD


def part_one(hands: list[Hand]) -> int:
    return sum((i+1)*hand.bid for i, hand in enumerate(sorted(hands)))


def part_two(hands: list[Hand]) -> int:
    joker_hands = [convert_jokers(hand) for hand in hands]
    return part_one(joker_hands)


def main():
    hands = load_hands("input/d07.txt")
    print(part_one(hands))
    print(part_two(hands))


if __name__ == "__main__":
    main()
