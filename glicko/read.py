from csv import DictReader
from datetime import datetime

from .league import League
from .game import Game
from .team import Team


def read_csv(csv_path: str) -> League:
    """
    Read a .csv of game data. Requirements:
    - Each game shows up exactly once (I'll do the flipping).
    - Each game is real (I'm not doing any filtering out 0-0 games)
    - Has the following columns:
        - home or team
        - away or opponent
        - home_score or score (float)
        - away_score or opponent_score (float)
        - round or week (int, start at 1)
        - season (int)
        - (optional) neutral site (defaults to None)
    """
    with open(csv_path) as f:
        rows = list(DictReader(f))
        games = []

        # Get all the teams
        team_names = set()
        for row in rows:
            team_names.add(row.get('home') or row['team'])
            team_names.add(row.get('away') or row['opponent'])
        team_lookup = {t: Team(t) for t in team_names}

        for row in rows:
            round_num = int(row.get('round') or row['week'])
            assert round_num > 0
            try:
                date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%MZ')
            except ValueError:
                date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%SZ')
            games.append(Game(
                team=team_lookup[row.get('home') or row['team']],
                opponent=team_lookup[row.get('away') or row['opponent']],
                team_score=float(row.get('home_score') or row['score']),
                opponent_score=float(row.get('away_score') or row['opponent_score']),
                season=int(row['season']),
                round_num=round_num,
                date=date,
                neutral_site=row.get('neutral_site')
            ))

    return League(games, list(team_lookup.values()))
