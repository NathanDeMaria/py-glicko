from csv import DictReader
from datetime import datetime

from .league import League
from .game import Game


def read_csv(csv_path: str) -> League:
    with open(csv_path) as f:
        csv_read = DictReader(f)
        games = []
        for row in csv_read:
            round_num = int(row['week'])
            assert round_num > 0
            date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%MZ')
            games.append(Game(
                team=row['team'],
                opponent=row['opponent'],
                team_score=float(row['score']),
                opponent_score=float(row['opponent_score']),
                season=int(row['season']),
                round=round_num,
                date=date,
                # TODO: fix little NFL-specific things
                group='NFL'
            ))

    return League(games)
