import numpy as np
from collections import defaultdict
from operator import itemgetter
from typing import Iterable, DefaultDict, List, Callable, Tuple

from .game import Game
from .league import League
from .team import Team
from .update import update_rating


FIRST = itemgetter(0)
Groups = DefaultDict[int, DefaultDict[int, DefaultDict[str, List[Game]]]]


# TODO: does it matter enough to np.array this?
def _pwp(score: float, opp_score: float) -> float:
    return (score ** 2) / (score ** 2 + opp_score ** 2)


def run_league(league: League,
               init_variance: float,
               variance_over_time: float = 0.,
               score_fn: Callable[[float, float], float] = _pwp
               ) -> Tuple[float, List[Team]]:

    team_lookup = {t: Team(t, init_variance) for t in league.team_names}

    def _build_results(games: Iterable[Game]) -> np.ndarray:
        return np.asarray([
            team_lookup[g.opponent].rating +
            (score_fn(g.team_score, g.opponent_score),)
            for g in games
        ])

    season_groups: Groups = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list)))
    for g in league.games:
        season_groups[g.season][g.round][g.team].append(g)

    total_discrepancy = 0.
    for season, round_groups in sorted(season_groups.items(), key=FIRST):
        for round_num, round_games in sorted(round_groups.items(), key=FIRST):
            for team_name, team_round_games in round_games.items():
                team = team_lookup[team_name]
                build_results = _build_results(team_round_games)
                updated, discrepancy = update_rating(
                    team.get_rating_before(season, round_num), build_results)
                total_discrepancy += discrepancy
                team.update_rating(updated, season, round_num)
        # Add variance increase in "offseason"
        for team in team_lookup.values():
            end_mean, end_var = team.get_rating_before(season + 1, 0)
            team.update_rating(
                (end_mean, end_var + variance_over_time),
                season + 1,
                0
            )

    return total_discrepancy, list(team_lookup.values())
