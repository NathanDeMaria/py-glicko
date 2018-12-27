import os
import pandas as pd
import numpy as np
from scipy.optimize import minimize

from glicko import run_league, read_csv
from glicko.league import League
from glicko.score import mov_cdf_builder


conferences_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'ncaaf_conferences.csv')
games_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'ncaaf.csv')


fbs_conferences = {
    # Power 5
    1, 4, 5, 8, 9,
    # Group of 5
    12, 15, 151, 17, 37,
    # Indep
    18,
}

conferences = pd.read_csv(conferences_path)
fbs_lookup = {
    row.team: (row.team_conf in fbs_conferences)
    for _, row in conferences.iterrows()
}


def is_fbs(team_name: str) -> bool:
    return fbs_lookup[team_name]


def create_offseason_runner(
    init_variance: float,
    variance_over_time: float,
    fbs_advantage: float,
):
    def run_offseason(l, season: int) -> None:
        for team in l.teams:
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
                team.update_rating(
                    (1500 + fbs_advantage * multiplier, init_variance),
                    season,
                    0
                )
    return run_offseason


def build_league(optimize: bool = False) -> League:
    league = read_csv(games_path)
    get_score = mov_cdf_builder(league)
    for g in league.games:
        g.set_score(get_score(g))

    best = [53976.233829140554, 37869.693762568044, 438.74162605181505]
    if optimize:
        def evaluate(x):
            r = create_offseason_runner(*x)
            return run_league(league, r)[0]

        result = minimize(
            evaluate,
            x0=np.array(best),
            options=dict(disp=True),
            bounds=((0, None), (0, None), (0, None))
        )
        best = list(result.x)

    runner = create_offseason_runner(*best)
    run_league(league, runner)
    return league
