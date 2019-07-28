import numpy as np
from collections import defaultdict
from itertools import groupby
from typing import (
    DefaultDict, Tuple, List, Iterable, Iterator, NamedTuple, Callable
)

from .game import Game
from .league import League
from .team import Team
from .update import update_rating, Rating


OffseasonRunner = Callable[[League, int], None]


class TeamRound(NamedTuple):
    season: int
    round_num: int
    team: Team
    round_games: Iterable[Game]
    season_games: Iterable[Game]

    @property
    def rating_before(self) -> Rating:
        return self.team.get_rating_before(self.season, self.round_num)

    @property
    def rating_before_season(self) -> Rating:
        return self.team.get_rating_before(self.season, 1)

    @property
    def round_results(self) -> np.ndarray:
        return np.asarray([
            game.opponent.get_rating_before(
                self.season, self.round_num)
            + (game.score,)
            for game in self.round_games
        ])

    @property
    def season_results(self) -> np.ndarray:
        opponent_results = []
        for game in self.season_games:
            # Get the opponent's rating this season so far, ignoring
            # the game against the current team.
            opponent_rating = game.opponent.get_rating_before(
                self.season, 1)
            opponent_games = game.opponent.games.get(self.season)
            if opponent_games:
                opponent_opponent_results = np.asarray([
                    opp_game.opponent.get_rating_before(
                        self.season, self.round_num)
                    + (opp_game.score,)
                    for opp_game in opponent_games
                    if opp_game.team != self.team
                    # _Should_ already be true, but just in case
                    # don't allow future games in here
                    and opp_game.round < self.round_num
                ])
                opponent_rating, _ = update_rating(
                    opponent_rating, opponent_opponent_results)
            opponent_results.append(opponent_rating + (game.score,))

        return np.asarray([opponent_results])


class Season(NamedTuple):
    season: int
    season_games: Iterable[Iterable[TeamRound]]


def create_basic_offseason_runner(
        init_variance: float = 1000,
        variance_over_time: float = 1000) -> OffseasonRunner:
    def run_offseason(league: League, season: int) -> None:
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
                team.update_rating((1500, init_variance), season, 0)
    return run_offseason


def run_league(
        league: League,
        run_offseason: OffseasonRunner = create_basic_offseason_runner(),
) -> Tuple[float, List[Team]]:
    for t in league.teams:
        t.reset()
    games = _group_games(league.games)
    discrepancy = 0.0
    for season in games:
        run_offseason(league, season.season)
        discrepancy += run_season(season.season_games)
    return discrepancy, league.teams


def run_season(games: Iterable[Iterable[TeamRound]]) -> float:
    return sum(run_round(round_games) for round_games in games)


def run_round(round_games: Iterable[TeamRound]) -> float:
    return sum(run_team_round(team_games) for team_games in round_games)


def run_team_round(team_round: TeamRound) -> float:
    # Find out how surprising this round's results were for this team
    # based on the team and opponents' ratings from the round before.
    _, discrepancy = update_rating(
        team_round.rating_before,
        team_round.round_results
    )

    # Update the team's rating based on
    # the results from the entire season so far
    # (against opponents' ratings from the round before).
    new_rating, _ = update_rating(
        team_round.rating_before_season,
        team_round.season_results
    )
    team_round.team.update_rating(
        new_rating, team_round.season, team_round.round_num)
    team_round.team.play_games(team_round.round_games)

    return discrepancy


def _group_games(games: List[Game]) -> Iterator[Season]:
    """
    Create groups where the first loop is over seasons,
    the second is over rounds, the third is teams.
    """
    def key(g: Game) -> Tuple[int, int, str]:
        return g.season, g.round, g.team.name
    games = sorted(games, key=key)

    for season, season_games in groupby(games, lambda g: g.season):
        season_game_lookup: DefaultDict[Team, List[Game]] = defaultdict(list)
        season_rounds = []
        for round_num, round_games in groupby(season_games, lambda g: g.round):
            grouped_round = groupby(round_games, lambda g: g.team)
            team_rounds = []
            for team, team_games in grouped_round:
                team_games_l = list(team_games)
                season_game_lookup[team].extend(team_games_l)
                team_round = TeamRound(
                    season, round_num, team,
                    team_games_l,
                    season_game_lookup[team].copy(),
                )
                team_rounds.append(team_round)
            season_rounds.append(team_rounds)
        yield Season(season, season_rounds)
