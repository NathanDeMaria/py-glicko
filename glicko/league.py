from typing import List

from .game import Game


class League:
    def __init__(self, games: List[Game]) -> None:
        self.team_names = set(g.team for g in games)
        self.team_names = self.team_names.union(g.opponent for g in games)
        self.games = games
        reversed_games = []
        for g in games:
            reversed_game = Game(
                g.opponent,
                g.team,
                g.opponent_score,
                g.team_score,
                g.season,
                g.round,
                g.date,
                g.group
            )
            reversed_games.append(reversed_game)
        self.games += reversed_games
