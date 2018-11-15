import os
import numpy as np
from collections import defaultdict
from scipy.optimize import minimize
from csv import DictReader

from glicko import run_league, read_csv
from glicko.league import League


conferences_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'ncaaf_conferences.csv')
games_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'ncaaf.csv')

fbs_conferences = {
    # Power 5
    1, 4, 5, 8, 9,
    # Group of 5
    12, 15, 151, 17, 37,
    # Independent
    18,
}

with open(conferences_path) as f:
    reader = DictReader(f)
    fbs_lookup = {
        row['team']: (row['team_conf'] in fbs_conferences)
        for row in reader
    }


def is_fbs(team_name: str) -> bool:
    return fbs_lookup[team_name]


def create_offseason_runner(
    init_variance: float,
    variance_over_time: float,
    fbs_advantage: float,
):
    def run_offseason(league, season: int) -> None:
        for team in league.teams:
            try:
                mean, var = team.rating
                team.update_rating(
                    (mean, var + variance_over_time),
                    season,
                    0
                )
            except ValueError:
                # i.e. this was the first season.
                multiplier = .5 if is_fbs(team.name) else -.5
                new_rating = (1500 + fbs_advantage * multiplier, init_variance)
                team.update_rating(new_rating, season, 0)
    return run_offseason


def build_league(optimize: bool = False) -> League:
    league = read_csv(games_path)

    init = [132651.43369133995, 23133.307212227475, 578.8213423010113]

    if optimize:
        def evaluate(x):
            r = create_offseason_runner(*x)

            # reset hack
            for t in league.teams:
                t._ratings = dict()
                t.games = defaultdict(list)

            return run_league(league, r)[0]

        result = minimize(
            evaluate,
            x0=np.array(init),
            options=dict(disp=True),
            bounds=((0, None), (0, None), (0, None))
        )

        init = list(result.x)

    runner = create_offseason_runner(*init)

    # reset hack
    for team in league.teams:
        team._ratings = dict()
        team.games = defaultdict(list)

    run_league(league, runner)
    return league
