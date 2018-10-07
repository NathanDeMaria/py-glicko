import numpy as np
from collections import defaultdict
from typing import Iterable, DefaultDict, List, Tuple, Set, Optional

from .game import Game
from .league import League
from .team import Team
from .update import update_rating


class Season:
    def __init__(self, games: List[Game]) -> None:
        self._season = games[0].season
        for g in games:
            assert g.season == self._season
        self._games = games

    @property
    def teams(self) -> Set[Team]:
        return set(g.team for g in self._games)

    @property
    def season_num(self) -> int:
        return self._season

    def get_games(self, team: Team,
                  ignore: Optional[Team] = None) -> Iterable[Game]:
        for g in self._games:
            if g.team == team and g.opponent != ignore:
                yield g


def run_league(league: League,
               init_variance: float,
               variance_over_time: float = 0.,
               n_iterations: int = 1) -> Tuple[float, List[Team]]:
    season_groups: DefaultDict[int, List[Game]] = defaultdict(list)
    for game in league.games:
        season_groups[game.season].append(game)
    first_season = min(season_groups.keys())
    for team in league.teams:
        team.update_rating((1500, init_variance), first_season, 0)
    seasons = [Season(games) for games in season_groups.values()]

    discrepancy = 0.
    for season in seasons:
        discrepancy += run_season(season, n_iterations)
        # Add variance increase in "offseason"
        for team in league.teams:
            end_mean, end_var = team.get_rating_before(
                season.season_num + 1, 0)
            team.update_rating(
                (end_mean, end_var + variance_over_time),
                season.season_num + 1,
                0
            )
    return discrepancy, league.teams


def run_season(season: Season, n_iterations: int) -> float:
    discrepancy = 0.
    for i in range(1, n_iterations + 1):
        discrepancy = _run_iteration(season, i)
    # Only from the last season
    return discrepancy


def _run_iteration(season: Season, i: int) -> float:
    # NOTE: embarrassingly || over teams
    total_discrepancy = 0.
    for team in season.teams:
        team_games = season.get_games(team)

        opponent_results = []
        for game in team_games:
            opponent_games = season.get_games(game.opponent, ignore=game.team)
            opponent_other_results = np.asarray([
                opp_game.opponent.get_rating_on(season.season_num, i - 1)
                + (opp_game.score,)
                for opp_game in opponent_games
            ])
            opponent_adjusted_rating, _ = update_rating(
                game.opponent.get_rating_on(season.season_num, i - 1),
                opponent_other_results
            )
            opponent_results.append(opponent_adjusted_rating + (game.score,))
        new_rating, discrepancy = update_rating(
            team.get_rating_on(season.season_num, i - 1),
            np.asarray(opponent_results)
        )
        team.update_rating(new_rating, season.season_num, i)
        total_discrepancy += discrepancy
    return total_discrepancy
