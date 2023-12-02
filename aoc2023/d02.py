from dataclasses import dataclass


@dataclass
class Round:
    red: int = 0
    blue: int = 0
    green: int = 0


@dataclass
class Game:
    id: int
    rounds: list[Round]


def parse_round(round_string: str) -> Round:
    # Extract from: "3 red, 4 green"
    groups = [group.strip().split(" ") for group in round_string.split(",")]
    counts = {colour: int(count) for count, colour in groups}
    return Round(green=counts.get("green", 0),
                 red=counts.get("red", 0),
                 blue=counts.get("blue", 0))


def parse_rounds(round_strings: str) -> [Round]:
    return [parse_round(round_string) for round_string in round_strings.split(";")]


def load_games(file_name) -> list[Game]:
    with open(file_name) as input_file:
        lines = [ln.replace("\n", "") for ln in input_file.readlines()]
        game_input = {game[5:]: rounds for game, rounds in [ln.split(":") for ln in lines]}
        return [Game(id=int(game_id),
                     rounds=parse_rounds(rounds)) for game_id, rounds in game_input.items()]


def game_valid_for_part_one(game: Game) -> bool:
    return all([all([g_round.red <= 12,
                     g_round.green <= 13,
                     g_round.blue <= 14]) for g_round in game.rounds])


def part_one(games: list[Game]) -> int:
    return sum(game.id for game in games if game_valid_for_part_one(game))


def game_power(game: Game) -> int:
    groups = [(g_round.red, g_round.green, g_round.blue) for g_round in game.rounds]
    red, blue, green = map(max, zip(*groups))
    return red*blue*green


def part_two(games: list[Game]) -> int:
    return sum(game_power(game) for game in games)


def main():
    games = load_games("input/d02.txt")
    print(part_one(games))
    print(part_two(games))


if __name__ == "__main__":
    main()
