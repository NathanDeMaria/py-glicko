import os
import numpy as np
from collections import defaultdict
from scipy.optimize import minimize

from glicko import run_league, read_csv
from glicko.better import League, create_basic_offseason_runner


CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nfl.csv')


def build_league(optimize: bool = False) -> League:
    league = read_csv(CSV_PATH)
    params = [10135.827392203391, 11418.893734148229]

    def evaluate(x):
        # reset hack
        for team in league.teams:
            team._ratings = dict()
            team.games = defaultdict(list)

        run_offseason = create_basic_offseason_runner(*x)
        return run_league(league, run_offseason)[0]

    if optimize:
        result = minimize(
            evaluate,
            x0=np.array(params),
            options=dict(disp=True),
            bounds=((0, None), (0, None))
        )

        params = list(result.x)

    run_league(league, create_basic_offseason_runner(*params))
    return league
