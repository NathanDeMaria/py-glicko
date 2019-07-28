from collections import defaultdict
from typing import Callable, Dict, DefaultDict, List

import numpy as np

from .league import League


OffseasonRunner = Callable[[League, int], None]


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


def create_grouped_offseason_runner(
        init_variance: float,
        variance_over_time: float
) -> OffseasonRunner:
    """
    Same as basic, except plus some logic so that teams added
    after the first season start with the average rating
    of the group they were put into.
    """
    def run_offseason(league: League, season: int) -> None:
        rating_lookup = _create_rating_lookup(league, season)
        for team in league.teams:
            try:
                mean, var = team.rating
                team.update_rating(
                    (mean, var + variance_over_time),
                    season,
                    0
                )
            except ValueError:
                # There's no rating for this team yet.
                group = team.get_group(season)
                if group is None:
                    # If the team didn't play in this season,
                    # we don't need to give them a rating yet.
                    continue
                group_rating = rating_lookup.get(group)
                if group_rating is None:
                    # TODO: handle if a group of totally new teams appears
                    raise NotImplementedError()
                team.update_rating((group_rating, init_variance), season, 0)
    return run_offseason


def _create_rating_lookup(league: League, season: int) -> Dict[str, float]:
    """
    :param league: A league full of teams with groups

    :returns: A lookup for group name -> average rating
    """
    ratings: DefaultDict[str, List[float]] = defaultdict(list)
    for team in league.teams:
        try:
            mean = team.rating[0]
            group = team.get_group(season)
            if group is not None:
                ratings[group].append(mean)
        except ValueError:
            # Team doesn't have a rating yet
            pass
    return {
        group: np.mean(group_ratings)
        for group, group_ratings in ratings.items()
    }
