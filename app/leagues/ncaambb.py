import os
import numpy as np
from scipy.optimize import minimize

from glicko import run_league, read_csv
from glicko.run import League, create_basic_offseason_runner
from glicko.score import hensley_cdf_builder


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ncaambb.csv'
)


def build_league(optimize: bool = False) -> League:
    league = read_csv(CSV_PATH)
    get_score = hensley_cdf_builder(league)
    for g in league.games:
        g.set_score(get_score(g))
    params = [54371.69206368768, 29815.254590976412]

    def evaluate(x):
        for team in league.teams:
            team.reset()

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
        print(params)

    run_league(league, create_basic_offseason_runner(*params))
    return league


if __name__ == '__main__':
    build_league(True)
