from csv import DictReader
from datetime import datetime

from .league import League
from .game import Game
from .team import Team


def read_csv(csv_path: str) -> League:
    with open(csv_path) as f:
        rows = list(DictReader(f))
        games = []

        # Get all the teams
        team_names = set()
        for row in rows:
            team_names.add(row['team'])
            team_names.add(row['opponent'])
        team_lookup = {t: Team(t) for t in team_names}

        for row in rows:
            round_num = int(row['week'])
            assert round_num > 0
            date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%MZ')
            games.append(Game(
                team=team_lookup[row['team']],
                opponent=team_lookup[row['opponent']],
                team_score=float(row['score']),
                opponent_score=float(row['opponent_score']),
                season=int(row['season']),
                round=round_num,
                date=date
            ))

    return League(games, list(team_lookup.values()))
