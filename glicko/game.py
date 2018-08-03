from dataclasses import dataclass
from datetime import datetime


@dataclass
class Game:
    team: str  # TODO: maybe don't need this? Or should this be the Team?
    opponent: str
    team_score: float
    opponent_score: float
    season: int
    round: int
    date: datetime
    group: str

    @property
    def score(self) -> float:
        # TODO: somewhere else?
        return ((self.team_score ** 2)
                / (self.team_score ** 2 + self.opponent_score ** 2))
