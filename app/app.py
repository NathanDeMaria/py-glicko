import os
import importlib.util
from collections import defaultdict
from flask import Flask, jsonify
from flask_cors import CORS
from typing import Dict, Optional, Tuple, List

from glicko.game import Game
from glicko.league import League


app = Flask(__name__)
CORS(app)


LEAGUE = 'ncaaf'


@app.route('/seasons')
def seasons():
    league = _get_league(LEAGUE)
    season_lookup = defaultdict(set)
    for g in league.games:
        season_lookup[g.season].add(g.round)
    # B/c sets aren't serializable
    season_lookup = {
        k: list(v) for k, v in season_lookup.items()
    }
    return jsonify(season_lookup)


class TeamRoundResult:
    def __init__(self, name: str,
                 current: Tuple[float, float],
                 previous: float,
                 week: int,
                 season_results: List[Game]) -> None:
        self.name = name
        self.current = current
        self.previous = previous
        self.game_results = []
        self.wins = 0
        self.losses = 0
        self.ties = 0
        for g in season_results:
            if g.round == week:
                self.game_results.append(dict(
                    opponent=g.opponent.name,
                    opponentScore=g.opponent_score,
                    score=g.team_score,
                ))
            if g.round <= week:
                if g.team_score > g.opponent_score:
                    self.wins += 1
                elif g.team_score < g.opponent_score:
                    self.losses += 1
                else:
                    self.ties += 1

        # Set later...srry
        self.rank = None
        self.previous_rank = None

    def to_dict(self) -> Dict:
        return dict(
            team=self.name,
            rating=self.current[0],
            variance=self.current[1],
            previousRating=self.previous,
            wins=self.wins,
            losses=self.losses,
            ties=self.ties,
            ranking=self.rank,
            previousRanking=self.previous_rank,
            gameResults=self.game_results,
        )


@app.route('/ratings/<int:season>/<int:week>')
def ratings(season: int, week: int):
    league = _get_league(LEAGUE)
    team_results = []
    for team in league.teams:
        previous = team.get_rating_before(season, week)
        try:
            current = team.get_rating_on(season, week)
        except KeyError:
            # Only happens on a bye week?
            current = previous
        team_games = team.games[season]
        team_results.append(TeamRoundResult(
            team.name,
            current,
            previous[0],
            week,
            team_games
        ))
    for i, team in enumerate(sorted(
            team_results, key=lambda t: t.previous, reverse=True)):
        team.previous_rank = i + 1
    sorted_teams = sorted(team_results,
                          key=lambda t: t.current[0],
                          reverse=True)
    for i, team in enumerate(sorted_teams):
        team.rank = i + 1

    return jsonify([t.to_dict() for t in sorted_teams])


def import_file(full_name, path):
    spec = importlib.util.spec_from_file_location(full_name, path)
    mod = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(mod)
    return mod


def find_leagues(league_dir: str = 'leagues') -> Dict[str, League]:
    league_files = os.listdir(league_dir)
    all_teams = dict()
    for league_file in league_files:
        if not league_file.endswith('.py'):
            continue
        fp = os.path.join(league_dir, league_file)
        league_name = league_file.split('.')[0]
        m = import_file('who cares?', fp)
        teams = m.build_league()
        all_teams[league_name] = teams
    return all_teams


def _get_league(league_name: str) -> Optional[League]:
    return ALL_LEAGUES.get(league_name)


if __name__ == '__main__':
    ALL_LEAGUES = find_leagues()
    app.run()
