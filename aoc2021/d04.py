import copy
from collections import namedtuple
from typing import List
from tools.file_loader import load_string_groups

Input = namedtuple("Input", ["numbers", "cards"])


class BingoCard:
    ROW_SIZE: int = 5

    def __init__(self, board: List[str]):
        self.board: List[List[int]] = [list(map(int, row.split())) for row in board]
        self.mask: List[List[int]] = [[1]*self.ROW_SIZE for i in range(self.ROW_SIZE)]

    def call_number(self, number: int) -> bool:
        for i in range(self.ROW_SIZE):
            for j in range(self.ROW_SIZE):
                if self.board[i][j] == number:
                    self.mask[i][j] = 0
        return self.board_complete()

    def board_complete(self):
        complete = False
        for row in self.mask:
            if sum(row) == 0:
                complete = True
        if not complete:
            for col in range(self.ROW_SIZE):
                total = 0
                for row in self.mask:
                    total += row[col]
                if total == 0:
                    complete = True
        return complete

    def uncalled_numbers(self):
        uncalled = []
        for i in range(self.ROW_SIZE):
            for j in range(self.ROW_SIZE):
                if self.mask[i][j] == 1:
                    uncalled.append(self.board[i][j])
        return uncalled


def load_input(path: str) -> Input:
    groups = load_string_groups(path)
    numbers = [int(num) for num in groups[0][0].split(",")]
    cards = [BingoCard(card) for card in groups[1:]]
    return Input(numbers=numbers, cards=cards)


GameResult = namedtuple("PartOne", ["winning_card", "final_number", "score"])


def part_one(game_input: Input) -> GameResult:
    winning_card = None
    game_round = 0
    cards: List[BingoCard] = copy.deepcopy(game_input.cards)
    while not winning_card:
        for card in cards:
            if card.call_number(game_input.numbers[game_round]):
                winning_card = card
        game_round += 1
    final_number = game_input.numbers[game_round - 1]
    score = sum(winning_card.uncalled_numbers()) * final_number

    return GameResult(winning_card=winning_card, final_number=final_number, score=score)


def part_two(game_input: Input) -> GameResult:
    call_number = 0
    cards: List[BingoCard] = copy.deepcopy(game_input.cards)
    winning_card = None
    while len(cards) != 0:
        next_cards = []
        for card in cards:
            if not card.call_number(game_input.numbers[call_number]):
                next_cards.append(card)
            else:
                winning_card = card
        cards = next_cards
        call_number += 1
    final_number = game_input.numbers[call_number - 1]
    score = sum(winning_card.uncalled_numbers()) * final_number

    return GameResult(winning_card=winning_card, final_number=final_number, score=score)


if __name__ == "__main__":
    def main():
        game_input = load_input("input/d04.txt")
        print(part_one(game_input))
        print(part_two(game_input))
    main()
