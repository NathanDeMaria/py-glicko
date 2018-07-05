from typing import List

from .game import Game


class League:
    def __init__(self, games: List[Game]) -> None:
        self.team_names = set(g.team for g in games)
        self.games = games
