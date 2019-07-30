import re
from collections import defaultdict
from functools import partial
from typing import (
    Callable, Dict, DefaultDict, List, Optional, Tuple, NamedTuple)

import numpy as np

from .league import League
from .team import Team


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
        get_new = partial(
            _get_new_rating,
            variance_over_time=variance_over_time,
            init_variance=init_variance,
            rating_lookup=rating_lookup,
        )

        # Hack: b/c seasons aren't necessarily zero indexed
        first_season = min(g.season for g in league.games)

        for team in league.teams:
            group = team.get_group(season)
            if season == first_season and group is not None:
                # It's the first season,
                # and this team played in the first season
                rating: Optional[Tuple[float, float]] = (1500., init_variance)
            else:
                rating = get_new(team, group)
            if rating:
                team.update_rating(rating, season, 0)
            
    return run_offseason


def create_grouped_spread_offseason_runner(
        init_variance: float,
        variance_over_time: float,
        **kwargs: float,
) -> OffseasonRunner:
    """
    Same as grouped, except the groups that appear in the first season
    don't all start with the same mean.

    Kwargs are the differences between leagues in the first season.
    """
    init_ratings = diffs_to_ratings(kwargs)
    
    def run_offseason(league: League, season: int) -> None:
        rating_lookup = _create_rating_lookup(league, season)
        get_new = partial(
            _get_new_rating,
            variance_over_time=variance_over_time,
            init_variance=init_variance,
            rating_lookup=rating_lookup,
        )

        # Hack: b/c seasons aren't necessarily zero indexed
        first_season = min(g.season for g in league.games)

        for team in league.teams:
            group = team.get_group(season)
            if season == first_season and group is not None:
                # It's the first season,
                # and this team played in the first season
                init_mean = init_ratings[group]
                rating: Optional[Tuple[float, float]] = (init_mean, init_variance)
            else:
                rating = get_new(team, group)
            if rating:
                team.update_rating(rating, season, 0)
            
    return run_offseason


class Diff(NamedTuple):
    from_group: str
    to_group: str
    diff: float

    @classmethod
    def from_item(cls, name: str, diff: float) -> 'Diff':
        match = re.match('(.*)_to_(.*)', name)
        if match is None:
            raise ValueError(f"Expected X_to_Y, but got {name}")
        from_group, to_group = match.groups()
        return cls(
            from_group=from_group,
            to_group=to_group,
            diff=diff,
        )


def diffs_to_ratings(diffs: Dict[str, float]) -> Dict[str, float]:
    diff_tuples = [Diff.from_item(name, diff) for name, diff in diffs.items()]
    ordered = [diff_tuples.pop(0)]
    while diff_tuples:
        for diff in diff_tuples:
            if ordered[0].from_group == diff.to_group:
                diff_tuples.remove(diff)
                ordered.insert(0, diff)
            elif ordered[-1].to_group == diff.from_group:
                diff_tuples.remove(diff)
                ordered.append(diff)
    
    offsets = np.cumsum([0.] + [d.diff for d in ordered])
    group_ratings = 1500. - offsets + offsets.mean()
    group_names = [ordered[0].from_group] + [d.to_group for d in ordered]
    return dict(zip(group_names, group_ratings))


def _get_new_rating(
        team: Team, group: Optional[str],
        variance_over_time: float, init_variance: float,
        rating_lookup: Dict[str, float]
) -> Optional[Tuple[float, float]]:
    try:
        mean, var = team.rating
        return mean, var + variance_over_time
    except ValueError:
        if group is None:
            # If the team didn't play in this season,
            # we don't need to give them a rating yet.
            return None
        group_rating = rating_lookup.get(group)
        if group_rating is None:
            group_rating = _get_new_group_rating(rating_lookup, group)
        return group_rating, init_variance


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
