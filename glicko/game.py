from datetime import datetime
from typing import Optional

from .team import Team


class Game:
    __slots__ = (
        'team', 'opponent',
        'team_score', 'opponent_score',
        'season', 'round', 'date', '_score',
    )

    def __init__(self, team: Team,
                 opponent: Team,
                 team_score: float,
                 opponent_score: float,
                 season: int,
                 round_num: int,
                 date: datetime,
                 score: Optional[float] = None) -> None:
        self.team = team
        self.opponent = opponent
        self.team_score = team_score
        self.opponent_score = opponent_score
        self.season = season
        self.round = round_num
        self.date = date
        self._score = score

    @property
    def score(self) -> float:
        if self._score is None:
            raise ValueError("Score not yet set")
        return self._score

    def set_score(self, value: float):
        if self._score is not None:
            raise ValueError("Cannot set score twice")
        self._score = value

    @property
    def flipped(self) -> 'Game':
        return Game(
            team=self.opponent,
            opponent=self.team,
            team_score=self.opponent_score,
            opponent_score=self.team_score,
            season=self.season,
            round_num=self.round,
            date=self.date,
            score=self._score
        )
