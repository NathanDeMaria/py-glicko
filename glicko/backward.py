import numpy as np
from collections import defaultdict
from typing import Iterable, DefaultDict, List, Tuple, Dict, Optional

from .game import Game
from .league import League
from .team import Team, Rating
from .update import update_rating


TeamLookup = Dict[str, Team]


class Season:
    def __init__(self, games: List[Game], team_lookup: TeamLookup):
        self._season = games[0].season
        for g in games:
            assert g.season == self._season
        self._games = games
        self._team_lookup = team_lookup

    @property
    def season_num(self) -> int:
        return self._season

    @property
    def teams(self) -> Iterable[Team]:
        return self._team_lookup.values()

    def get_games(self, team: str,
                  ignore: Optional[str] = None) -> Iterable[Game]:
        for g in self._games:
            if g.team == team and g.opponent != ignore:
                yield g

    def get_rating(self, team: str, iteration: int) -> Rating:
        return self._team_lookup[team].get_rating_on(self._season, iteration)

    def set_rating(self, team: str, iteration: int, rating: Rating) -> None:
        self._team_lookup[team].update_rating(rating, self._season, iteration)


def run_league(league: League,
               init_variance: float,
               variance_over_time: float = 0.,
               n_iterations: int = 1) -> Tuple[float, List[Team]]:
    team_lookup = {
        t: Team(t, init_variance)
        for t in league.team_names
    }
    season_groups: DefaultDict[List[Game]] = defaultdict(list)
    for game in league.games:
        season_groups[game.season].append(game)
    seasons = [
        Season(games, team_lookup)
        for games in season_groups.values()
    ]

    discrepancy = 0
    for season in seasons:
        discrepancy += run_season(season, n_iterations)
        # Add variance increase in "offseason"
        for team in team_lookup.values():
            end_mean, end_var = team.get_rating_before(
                season.season_num + 1, 0)
            team.update_rating(
                (end_mean, end_var + variance_over_time),
                season.season_num + 1,
                0
            )
    return discrepancy, list(team_lookup.values())


def run_season(season: Season, n_iterations: int) -> float:
    discrepancy = 0
    for i in range(1, n_iterations + 1):
        discrepancy = run_iteration(season, i)
    # Only from the last season
    return discrepancy


def run_iteration(season: Season, i: int) -> float:
    # Assuming the previous iteration has been marked on ``league_tracker``
    # NOTE: embarrassingly || over teams
    total_discrepancy = 0
    for team in season.teams:
        team_games = season.get_games(team.name)

        opponent_results = []
        for game in team_games:
            opponent_games = season.get_games(game.opponent, ignore=game.team)
            opponent_other_results = np.asarray([
                season.get_rating(opp_game.opponent, i - 1) + (opp_game.score,)
                for opp_game in opponent_games
            ])
            opponent_adjusted_rating, _ = update_rating(
                season.get_rating(game.opponent, i - 1), opponent_other_results
            )
            opponent_results.append(opponent_adjusted_rating + (game.score,))
        new_rating, discrepancy = update_rating(
            season.get_rating(team.name, i - 1), np.asarray(opponent_results)
        )
        team.update_rating(new_rating, season.season_num, i)
        total_discrepancy += discrepancy
    return total_discrepancy
