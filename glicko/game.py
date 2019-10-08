from datetime import datetime
from typing import Optional

from .team import Team


class Game:
    """
    Parameters
    ----------
    neutral_site
        True if the game was at a neutral site,
        None if this data-set doesn't report/care
    """
    __slots__ = (
        'team', 'opponent',
        'team_score', 'opponent_score',
        'season', 'round', 'date', '_score',
        'neutral_site',
    )

    def __init__(self, team: Team,
                 opponent: Team,
                 team_score: float,
                 opponent_score: float,
                 season: int,
                 round_num: int,
                 date: datetime,
                 score: Optional[float] = None,
                 neutral_site: Optional[bool] = None) -> None:
        self.team = team
        self.opponent = opponent
        self.team_score = team_score
        self.opponent_score = opponent_score
        self.season = season
        self.round = round_num
        self.date = date
        _assert_score_is_valid(score)
        self._score = score
        self.neutral_site = neutral_site

    @property
    def score(self) -> float:
        if self._score is None:
            raise ValueError("Score not yet set")
        return self._score

    def set_score(self, value: float):
        _assert_score_is_valid(value)
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
            score=None if self._score is None else 1 - self._score,
            neutral_site=self.neutral_site,
        )


def _assert_score_is_valid(score: Optional[float]):
    if score is None:
        return
    if 0 <= score <= 1:
        return
    raise ValueError(f"Invalid score: {score}. Must be [0, 1]")
