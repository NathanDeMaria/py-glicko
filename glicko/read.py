from collections import defaultdict
from csv import DictReader
from datetime import datetime
from dateutil import parser
from typing import DefaultDict, Dict, List, Tuple

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

        # Get all the teams
        team_names = set()
        for row in rows:
            team_names.add(row.get('home') or row['team'])
            team_names.add(row.get('away') or row['opponent'])
        team_lookup = {t: Team(t) for t in team_names}

        games = [_to_game(row, team_lookup) for row in rows]

    return League(games, list(team_lookup.values()))


def read_csvs(game_csv: str, team_csv: str) -> League:
    """
    CSV for games is formatted the same as for `read_csv`.
    CSV for teams has 3 columns: team name, season, and "group"
    """
    with open(team_csv) as f:
        teams: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)
        for row in DictReader(f):
            teams[row['name']].append((int(row['season']), row['group']))
    team_lookup = {
        name: Team(name, dict(groups)) for name, groups in teams.items()
    }
    with open(game_csv) as f:
        games = [_to_game(row, team_lookup) for row in DictReader(f)]
    return League(games, list(team_lookup.values()))


def _to_game(row: Dict, team_lookup: Dict[str, Team]):
    round_num = int(row.get('round') or row['week'])
    assert round_num > 0
    date = parser.parse(row['date'])
    neutral_site = row.get('neutral_site')
    return Game(
        team=team_lookup[row.get('home') or row['team']],
        opponent=team_lookup[row.get('away') or row['opponent']],
        team_score=float(row.get('home_score') or row['score']),
        opponent_score=float(row.get('away_score') or row['opponent_score']),
        season=int(row['season']),
        round_num=round_num,
        date=date,
        neutral_site=None if neutral_site is None else bool(neutral_site),
    )
