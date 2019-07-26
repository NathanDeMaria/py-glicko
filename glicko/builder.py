import numpy as np
from scipy.optimize import minimize
from typing import Callable, List

from .league import League
from .run import create_basic_offseason_runner, OffseasonRunner, run_league
from .score import ScoreFunction, hensley_cdf_builder


# TODO: can I be specific about the arg type here?
OffseasonRunnerBuilder = Callable[..., OffseasonRunner]
ScoreFunctionBuilder = Callable[[League], ScoreFunction]


class LeagueBuilder:
    """
    :param score_function_builder: Function that looks at all games in order to
        figure out how to give each one a 0-1 score.
    :param offseason_runner_builder: Function that takes tunable scalar
        hyperparameters that creates a function which manages
        updates to the league in between seasons
        (think increasing variance over time, handle new teams added, etc.)
    """
    def __init__(
            self,
            league: League,
            default_params,
            score_function_builder: ScoreFunctionBuilder = hensley_cdf_builder,
            offseason_runner_builder = create_basic_offseason_runner,
    ):
        self._league = league
        self._params = default_params
        get_score = score_function_builder(league)
        for g in league.games:
            g.set_score(get_score(g))
        self._offseason_runner_builder = offseason_runner_builder
    
    def optimize(self) -> List[float]:
        def evaluate(x):
            for team in self._league.teams:
                team.reset()

            run_offseason = self._offseason_runner_builder(*x)
            return run_league(self._league, run_offseason)[0]

        result = minimize(
            evaluate,
            x0=np.array(self._params),
            options=dict(disp=True),
            bounds=[(0, None) for _ in self._params]
        )
        self._params = list(result.x)
        return self._params
    
    def get_league(self) -> League:
        for team in self._league.teams:
            team.reset()
        run_league(self._league, create_basic_offseason_runner(*self._params))
        return self._league
