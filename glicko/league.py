from typing import List

from .game import Game
from .team import Team


class League:
    def __init__(self, games: List[Game], teams: List[Team] = None, home_only: bool = True) -> None:
        """
        :param games: list of games
        :param teams: list of teams, will be pulled from teams on games if none are provided
        :param home_only: leave as true if each game only shows up once.
            Set to false if the games list already has the "flipped" games
        """
        self.games = games
        reversed_games = []
        if home_only:
            for g in games:
                reversed_game = g.flipped
                reversed_games.append(reversed_game)
        self.games += reversed_games

        if teams is None:
            # This might just be for easier tests?
            teams = list(set(g.team for g in self.games))
        self.teams: List[Team] = teams
