import numpy as np
from collections import defaultdict
from operator import itemgetter
from typing import Iterable, DefaultDict, List, Callable, Tuple, Dict

from .game import Game
from .league import League
from .team import Team
from .update import update_rating


FIRST = itemgetter(0)
Groups = DefaultDict[int, DefaultDict[str, List[Game]]]
ScoreFunction = Callable[[float, float], float]


# TODO: does it matter enough to np.array this?
def _pwp(score: float, opp_score: float) -> float:
    return (score ** 2) / (score ** 2 + opp_score ** 2)


def run_league(league: League,
               init_variance: float,
               variance_over_time: float = 0.,
               n_iterations: int = 1,
               score_fn: ScoreFunction = _pwp
               ) -> Tuple[float, List[Team]]:

    team_lookup: Dict[str, Team] = {
        t: Team(t, init_variance)
        for t in league.team_names
    }

    def _build_results(games: Iterable[Game], s: int, r: int) -> np.ndarray:
        return np.asarray([
            team_lookup[g.opponent].get_rating_before(s, r) +
            (score_fn(g.team_score, g.opponent_score),)
            for g in games
        ])

    season_groups: Groups = defaultdict(lambda: defaultdict(list))
    for game in league.games:
        season_groups[game.season][game.team].append(game)

    total_discrepancy = 0.
    for season, team_seasons in sorted(season_groups.items(), key=FIRST):
        discrepancy = 0
        for i in range(1, n_iterations + 1):
            discrepancy = 0.
            for team_name, team_games in team_seasons.items():
                discrepancy += _run_team_iteration(_build_results, i, score_fn, season, team_games, team_lookup, team_name, team_seasons)
        # Only bump the discrepancy for the last iteration
        total_discrepancy += discrepancy
        # Add variance increase in "offseason"
        for team in team_lookup.values():
            end_mean, end_var = team.get_rating_before(season + 1, 0)
            team.update_rating(
                (end_mean, end_var + variance_over_time),
                season + 1,
                0
            )
    return total_discrepancy, list(team_lookup.values())


def _run_team_iteration(_build_results, i, score_fn, season, team_games,
                        team_lookup, team_name, team_seasons):
    team = team_lookup[team_name]
    game_results = []
    for game in team_games:
        # Get the opponent's (i-1) rating,
        # for games excluding ones against the current team
        opponent = team_lookup[game.opponent]
        previous_opp_rating = opponent.get_rating_before(season, i)
        opponent_games = [
            g for g in team_seasons[game.opponent]
            if g.opponent != team_name
        ]
        games_array = _build_results(opponent_games, season, i)
        new_rating, _ = update_rating(
            previous_opp_rating, games_array)
        game_results.append(
            (*new_rating,
             score_fn(game.team_score, game.opponent_score))
        )
    game_results = np.array(game_results)
    new_rating, team_discrepancy = update_rating(
        team.rating, game_results)
    team.update_rating(new_rating, season, i)
    return team_discrepancy
