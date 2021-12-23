from dataclasses import dataclass
from typing import Iterator, Set, Type, Dict


class Unhandled(Exception):
    pass


def get_new_deterministic_die() -> Iterator[int]:
    def roll():
        die = 1
        while True:
            yield die
            die = die % 100 + 1
    return roll()


@dataclass
class Player:
    space: int
    score: int = 0


@dataclass
class Game:
    player_1: Player
    player_2: Player
    rolls: int = 0

    def __hash__(self):
        my_hash = self.rolls % 6
        my_hash *= 100
        my_hash += self.player_1.score
        my_hash *= 100
        my_hash += self.player_1.space
        my_hash *= 100
        my_hash += self.player_2.score
        my_hash *= 100
        my_hash += self.player_2.space
        return my_hash


def advance_player(player: Player, die: Iterator[int]):
    steps = (next(die) + next(die) + next(die)) % 10
    player.space = player.space + steps
    if player.space > 10:
        player.space -= 10
    player.score += player.space


def play(die: Iterator[int], game: Game):
    while game.player_1.score < 1000 and game.player_2.score < 1000:
        advance_player(game.player_1, die)
        game.rolls += 3
        if game.player_1.score < 1000:
            advance_player(game.player_2, die)
            game.rolls += 3


def score_game(game):
    return min(game.player_1.score, game.player_2.score) * game.rolls


@dataclass
class TimeStream:
    num_universes: int
    total: int

    def __lt__(self, other: Type['TimeStream']):
        return self.total < other.total

    def __hash__(self):
        return self.total


def possible_rolls() -> Set[TimeStream]:
    rolls: Dict[int, int] = {}
    for x in range(3):
        for y in range(3):
            for z in range(3):
                total = 3+x+y+z
                if total in rolls:
                    rolls[total] += 1
                else:
                    rolls[total] = 1
    return {TimeStream(total=total, num_universes=count) for total, count in rolls.items()}


@dataclass
class Multiverse:
    player1_victories: Dict[Game, int]
    player2_victories: Dict[Game, int]
    in_play: Dict[Game, int]


def run_dirac_game(multiverse: Multiverse):
    time_streams = possible_rolls()
    while multiverse.in_play:
        in_play, count = next(iter(multiverse.in_play.items()))
        del multiverse.in_play[in_play]
        for child_universe, num_children in dirac_turn(in_play, time_streams).items():
            net_children = num_children * count
            if child_universe in multiverse.player1_victories:
                multiverse.player1_victories[child_universe] += net_children
            elif child_universe in multiverse.player2_victories:
                multiverse.player2_victories[child_universe] += net_children
            elif child_universe in multiverse.in_play:
                multiverse.in_play[child_universe] += net_children
            elif child_universe.player_1.score >= 21:
                multiverse.player1_victories[child_universe] = net_children
            elif child_universe.player_2.score >= 21:
                multiverse.player2_victories[child_universe] = net_children
            else:
                multiverse.in_play[child_universe] = net_children


def starting_universe(player1_start: int, player2_start: int):
    universe = Game(
        rolls=0,
        player_1=Player(score=0, space=player1_start),
        player_2=Player(score=0, space=player2_start),
    )
    return Multiverse(
        player1_victories={},
        player2_victories={},
        in_play={universe: 1}
    )


def advance_space(space: int, to_move: int) -> int:
    space += (to_move % 10)
    if space > 10:
        space -= 10
    return space


def advance_and_score_player(player: Player, to_move: int):
    player.space = advance_space(player.space, to_move)
    player.score += player.space


def clone_game(game: Game) -> Game:
    return Game(
        rolls=game.rolls,
        player_1=Player(space=game.player_1.space, score=game.player_1.score),
        player_2=Player(space=game.player_2.space, score=game.player_2.score)
    )


def dirac_turn(game: Game, time_streams: Set[TimeStream]) -> Dict[Game, int]:
    new_games = {}
    for time_stream in time_streams:
        new_game = clone_game(game)
        if game.rolls % 6 == 0:
            advance_and_score_player(new_game.player_1, time_stream.total)
        elif game.rolls % 6 == 3:
            advance_and_score_player(new_game.player_2, time_stream.total)
        else:
            raise Unhandled
        new_game.rolls += 3
        if new_game in new_games:
            new_games[new_game] += time_stream.num_universes
        else:
            new_games[new_game] = time_stream.num_universes
    return new_games


if __name__ == "__main__":
    def main():
        game = Game(player_1=Player(space=4), player_2=Player(space=8))
        play(get_new_deterministic_die(), game)
        print(game)
        print(score_game(game))
        the_game = starting_universe(8, 10)
        run_dirac_game(the_game)
        player1_wins = sum(num_universes for _, num_universes in the_game.player1_victories.items())
        player2_wins = sum(num_universes for _, num_universes in the_game.player2_victories.items())
        print(f"Player 1: {player1_wins}")
        print(f"Player 2: {player2_wins}")
    main()
