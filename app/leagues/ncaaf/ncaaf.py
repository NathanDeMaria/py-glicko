import os
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from typing import Optional, Tuple

from endgame_matcher import Translator
from glicko import Parameter, LeagueBuilder
from glicko.read import read_csvs, League
from glicko.offseason import diffs_to_ratings, _create_rating_lookup, OffseasonRunner, partial, _get_new_rating


PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBDIVISIONS_PATH = os.path.join(PARENT_DIR, 'ncaaf_subdivisions.csv')
GAMES_PATH = os.path.join(PARENT_DIR, 'ncaaf.csv')
ESPN_TEAMS_FILE = os.path.join(PARENT_DIR, 'ncaaf_team_info.csv')
SPORTS247_FILE = os.path.join(PARENT_DIR, 'ncaaf_recruiting.csv')
PARAMS_FILE = os.path.join(PARENT_DIR, 'ncaaf.json')

espn_teams = pd.read_csv(ESPN_TEAMS_FILE)
translator = Translator(set(espn_teams.espn_location))

sports247 = pd.read_csv(SPORTS247_FILE)
sports247['espn_location'] = [translator.translate(n) for n in sports247.name]
sports247 = sports247[[l is not None for l in sports247.espn_location]]
sports247['espn_display_name'] = [espn_teams.espn_display_name[espn_teams.espn_location == l].iloc[0] for l in sports247.espn_location]
sports247['espn_name'] = [' '.join([row['espn_location'], row['espn_display_name']]) for _, row in sports247.iterrows()]

sports247['norm_rating'] = sports247.groupby('year').transform(lambda x: (x - x.mean()) / x.std())


def create_grouped_spread_offseason_runner_with_recruiting(
        init_variance: float,
        variance_over_time: float,
        recruiting_weight: float,
        recruiting_weight2: float,
        recruiting_weight3: float,
        recruiting_weight4: float,
        recruiting_weight5: float,
        recruiting_weight6: float,
        **kwargs: float,
) -> OffseasonRunner:
    """
    Same as grouped, except the groups that appear in the first season
    don't all start with the same mean.

    Kwargs are the differences between leagues in the first season.
    """
    init_ratings = diffs_to_ratings(kwargs)
    
    def run_offseason(league: League, season: int) -> None:
        rating_lookup = _create_rating_lookup(league, season)
        get_new = partial(
            _get_new_rating,
            variance_over_time=variance_over_time,
            init_variance=init_variance,
            rating_lookup=rating_lookup,
        )

        # Hack: b/c seasons aren't necessarily zero indexed
        first_season = min(g.season for g in league.games)

        for team in league.teams:
            group = team.get_group(season)
            if season == first_season and group is not None:
                # It's the first season,
                # and this team played in the first season
                init_mean = init_ratings[group]
                rating: Optional[Tuple[float, float]] = (init_mean, init_variance)
            else:
                rating = get_new(team, group)
            if rating:
                m, sd = rating
                m = (
                    m +
                    get_recruiting_rating(team.name, season) * recruiting_weight +
                    get_recruiting_rating(team.name, season - 1) * recruiting_weight2 +
                    get_recruiting_rating(team.name, season - 2) * recruiting_weight3 +
                    get_recruiting_rating(team.name, season - 3) * recruiting_weight4 +
                    get_recruiting_rating(team.name, season - 4) * recruiting_weight5 +
                    get_recruiting_rating(team.name, season - 5) * recruiting_weight6
                )
                team.update_rating((m, sd), season, 0)
            
    return run_offseason


full_league = read_csvs(GAMES_PATH, SUBDIVISIONS_PATH)
team_seasons = defaultdict(Counter)
for g in full_league.games:
    team_seasons[g.team][g.season] += 1
real_teams = []
for team, season_counts in team_seasons.items():
    full_seasons = len([c for c in season_counts.values() if c >= 10])
    if full_seasons >= 14:
        real_teams.append(team)
real_team_names = set(t.name for t in real_teams)
real_games = []
for game in full_league.games:
    if (game.team.name in real_team_names
            and game.opponent.name in real_team_names
            and (game.team_score or game.opponent_score)):
        real_games.append(game)

league = League(real_games, home_only=False)
def _get_recruiting_rating(name, season):
    matching_rows = sports247[np.logical_and(
        sports247.espn_name == name,
        sports247.year == season)
    ].norm_rating
    
    if len(matching_rows) == 0:
        return sports247[sports247.year == season].norm_rating.min()
    return matching_rows.iloc[0]

recruiting_lookup = defaultdict(list)
first_season = min(g.season for g in league.games)
last_season = max(g.season for g in league.games)
for season in range(first_season, last_season + 1):
    for t in league.teams:
        recruiting_lookup[t.name].append(_get_recruiting_rating(t.name, season))

        
def get_recruiting_rating(name, season):
    if season - first_season < 0:
        return 0
    return recruiting_lookup[name][season - first_season]


max_diff = 1000.
recruiting_width = 100.
params = [
    Parameter(
        name='init_variance',
        value=20000.,
        bounds=[1.0, 1e6],
    ),
    Parameter(
        name='variance_over_time',
        value=20000.,
        bounds=[1.0, 1e5],
    ),
    Parameter(
        name='recruiting_weight',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='recruiting_weight2',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='recruiting_weight3',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='recruiting_weight4',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='recruiting_weight5',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='recruiting_weight6',
        value=0.,
        bounds=[-recruiting_width, recruiting_width],
    ),
    Parameter(
        name='1fbs_to_2fcs',
        value=100.,
        bounds=[0, max_diff],
    ),
    Parameter(
        name='2fcs_to_3d2',
        value=100.,
        bounds=[0, max_diff],
    ),
]

builder = LeagueBuilder(
    league, params,
    offseason_runner_builder=create_grouped_spread_offseason_runner_with_recruiting
)
if os.path.exists(PARAMS_FILE):
    builder.load_parameters(PARAMS_FILE)


if __name__ == '__main__':
    builder.optimize(total_trials=100)
    builder.save_parameters(PARAMS_FILE)
