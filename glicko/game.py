from dataclasses import dataclass
from datetime import datetime

from .team import Team


@dataclass
class Game:
    team: Team
    opponent: Team
    team_score: float
    opponent_score: float
    season: int
    round: int
    date: datetime

    @property
    def score(self) -> float:
        # TODO: somewhere else?
        return ((self.team_score ** 2)
                / (self.team_score ** 2 + self.opponent_score ** 2))

    @property
    def flipped(self) -> 'Game':
        return Game(
            team=self.opponent,
            opponent=self.team,
            team_score=self.opponent_score,
            opponent_score=self.team_score,
            season=self.season,
            round=self.round,
            date=self.date,
        )
