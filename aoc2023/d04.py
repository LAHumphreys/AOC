from dataclasses import dataclass
from tools.list_ops import non_sorted_intersection


@dataclass
class Card:
    id: int
    card_numbers: list[int]
    winning_numbers: list[int]


def get_winning(card: Card) -> list[int]:
    return non_sorted_intersection(card.winning_numbers, card.card_numbers)


def parse_card(line: str) -> Card:
    id_string, numbers_string = line.split(":")
    card_num_string, winning_string = numbers_string.split("|")
    return Card(id=int(id_string.strip().split()[-1]),
                winning_numbers=[int(i) for i in winning_string.strip().split()],
                card_numbers=[int(i) for i in card_num_string.strip().split()])


def load_cards(filename: str) -> list[Card]:
    with open(filename, encoding='utf-8') as input_file:
        lines = (line.replace("\n", "") for line in input_file.readlines())
        return [parse_card(line) for line in lines]


def part_one(cards: list[Card]) -> int:
    winners = filter(lambda n: n, (get_winning(card) for card in cards))
    return sum(2**(len(win)-1) for win in winners)


def part_two(cards: list[Card]) -> int:
    card_count = {card.id: 1 for card in cards}
    while cards:
        card = cards.pop(0)
        num_this_card = card_count[card.id]
        for won_card in cards[0:len(get_winning(card))]:
            card_count[won_card.id] += num_this_card

    return sum(card_count.values())


def main():
    cards = load_cards("input/d04.txt")
    print(part_one(cards))
    print(part_two(cards))


if __name__ == "__main__":
    main()
