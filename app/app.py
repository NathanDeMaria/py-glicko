import os
import sys
import importlib.util
from collections import defaultdict
from flask import Flask, jsonify
from flask_cors import CORS
from typing import Dict, Optional, Tuple, List

from glicko.game import Game
from glicko.league import League


app = Flask(__name__)
CORS(app)


def get_league(league_name: str) -> League:
    return ALL_LEAGUES.get(league_name)


def build_season_lookup(league: League) -> Dict[int, List[int]]:
    season_lookup = defaultdict(set)
    for g in league.games:
        season_lookup[g.season].add(g.round)
    # B/c sets aren't serializable
    return {
        k: list(v) for k, v in season_lookup.items()
    }


@app.route('/<league_name>/seasons')
def seasons(league_name: str):
    league = get_league(league_name)
    if not league:
        return jsonify(), 404
    season_lookup = build_season_lookup(league)
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


@app.route('/<league_name>/ratings/<int:season>/<int:week>')
def ratings(league_name: str, season: int, week: int):
    league = get_league(league_name)
    if not league:
        return jsonify(), 404
    team_results = []

    # if they're null??
    if not season and not week:
        season = max(g.season for g in league.games)
        week = max(g.round for g in league.games if g.season == season)

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


@app.route('/<league_name>/team/<team_name>')
def get_team_history(league_name: str, team_name: str):
    league = get_league(league_name)
    if not league:
        return jsonify(), 404
    team = None
    # Maybe turn this into a lookup...
    for t in league.teams:
        if t.name.replace(' ', '') == team_name:
            team = t
            break
    if not team:
        return jsonify(), 404

    season_lookup = build_season_lookup(league)
    history = []
    for s, rounds in season_lookup.items():
        for r in rounds:
            try:
                mean, variance = team.get_rating_on(s, r)
                history.append(dict(
                    mean=mean,
                    variance=variance,
                    season=s,
                    round=r,
                ))
            except KeyError:
                pass
    return jsonify(history)


@app.route('/leagues')
def get_leagues():
    return jsonify(list(ALL_LEAGUES.keys()))


@app.route('/<league_name>/teams')
def get_teams(league_name: str):
    league = get_league(league_name)
    if not league:
        return jsonify(), 404

    teams = [t.name for t in league.teams]
    return jsonify(teams)


def import_file(full_name, path):
    file_location = path
    if not file_location.endswith('.py'):
        file_location = os.path.join(file_location, '__init__.py')
    spec = importlib.util.spec_from_file_location(full_name, file_location)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def find_leagues(league_dir: str = 'leagues') -> Dict[str, League]:
    league_files = os.listdir(league_dir)
    all_teams = dict()
    for league_file in league_files:
        # TODO: revive other leagues
        if not any(league_file.startswith(n) for n in {'ncaaf', 'nfl'}):
            continue
        fp = os.path.join(league_dir, league_file)
        league_name = league_file.split('.')[0]
        m = import_file(league_name, fp)
        teams = m.builder.get_league()
        all_teams[league_name] = teams
    return all_teams


def _get_league(league_name: str) -> Optional[League]:
    return ALL_LEAGUES.get(league_name)


if __name__ == '__main__':
    ALL_LEAGUES = find_leagues()
    app.run(host='0.0.0.0')
