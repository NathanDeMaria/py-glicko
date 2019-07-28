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

        # Hack: b/c seasons aren't necessarily zero indexed
        first_season = min(g.season for g in league.games)

        for team in league.teams:
            if season == first_season and team.get_group(season) is not None:
                # It's the first season,
                # and this team played in the first season
                team.update_rating((1500., init_variance), season, 0)
            else:
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
                        group_rating = _get_new_group_rating(rating_lookup, group)
                    team.update_rating((group_rating, init_variance), season, 0)
    return run_offseason


def _get_new_group_rating(rating_lookup: Dict[str, float], group: str) -> float:
    """
    Assuming the group names are in some relevant lexicographical order,
    grab the ratings of the nearest groups alphabetically.

    If it's between two groups, take the average.
    If it's off either end of the list, take the closest.
    """
    sorted_ratings = sorted(rating_lookup.items(), key=lambda kv: kv[0])
    i = 0
    for i, (g, _) in enumerate(sorted_ratings):
        if g > group:
            break
    else:
        # Runs if for executes without breaking, making i the index
        # group would belong if inserted into the list of ratings
        i += 1
    
    if i == 0:
        return sorted_ratings[0][1]
    if i >= len(sorted_ratings):
        return sorted_ratings[-1][1]
    return (sorted_ratings[i][1] + sorted_ratings[i - 1][1]) / 2


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
