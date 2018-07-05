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
