import numpy as np
from ax import optimize
from typing import Callable, Dict, List, NamedTuple

from .league import League
from .run import create_basic_offseason_runner, OffseasonRunner, run_league
from .score import ScoreFunction, hensley_cdf_builder


# TODO: can I be specific about the arg type here?
OffseasonRunnerBuilder = Callable[..., OffseasonRunner]
ScoreFunctionBuilder = Callable[[League], ScoreFunction]


class Parameter(NamedTuple):
    name: str
    bounds: List[float]
    value: float
    param_type: str = 'range'
    
    def update_value(self, value: float) -> 'Parameter':
        d = self._asdict()
        d.pop('value')
        return Parameter(
            value=value,
            **d
        )

    def to_dict(self) -> Dict:
        return dict(
            name=self.name,
            type=self.param_type,
            bounds=self.bounds,
        )


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
            params: List[Parameter],
            score_function_builder: ScoreFunctionBuilder = hensley_cdf_builder,
            offseason_runner_builder = create_basic_offseason_runner,
    ):
        self._league = league
        self._params = {p.name: p for p in params}
        get_score = score_function_builder(league)
        for g in league.games:
            g.set_score(get_score(g))
        self._offseason_runner_builder = offseason_runner_builder
    
    def optimize(self):
        def evaluate(kwargs: Dict[str, float]):
            run_offseason = self._offseason_runner_builder(**kwargs)
            return run_league(self._league, run_offseason)[0]

        best_parameters, best_values, experiment, model = optimize(
            parameters=[p.to_dict() for p in self._params.values()],
            evaluation_function=evaluate,
            minimize=True
        )
        for name, best_value in best_parameters.items():
            self._params[name] = self._params[name].update_value(best_value)
        self._params = best_parameters
        return best_parameters, best_values, experiment, model
    
    def get_league(self) -> League:
        run_offseason = self._offseason_runner_builder(**{
            name: p.value for name, p in self._params.items()
        })
        run_league(self._league, run_offseason)
        return self._league
