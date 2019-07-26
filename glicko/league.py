from typing import List

from .game import Game
from .team import Team


class League:
    def __init__(self, games: List[Game], teams: List[Team] = None) -> None:
        self.games = games
        reversed_games = []
        for g in games:
            reversed_game = g.flipped
            reversed_games.append(reversed_game)
        self.games += reversed_games

        if teams is None:
            # This might just be for easier tests?
            teams = list(set(g.team for g in self.games))
        self.teams: List[Team] = teams
