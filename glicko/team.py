from collections import defaultdict
from typing import Dict, Tuple, Iterator, Optional, List

Rating = Tuple[float, float]
Time = Tuple[int, int]


class Team:
    def __init__(self, name: str, groups: Dict[int, str] = None) -> None:
        self._name = name
        self._ratings: Dict[int, Dict[int, Rating]] = {}
        self.games: Dict[int, List] = defaultdict(list)
        self._groups = groups

    @property
    def name(self) -> str:
        return self._name

    def update_rating(self, rating: Rating, season: int,
                      round_number: int) -> None:
        # TODO: be better
        if season not in self._ratings:
            self._ratings[season] = dict()
        self._ratings[season][round_number] = rating

    # TODO: should I just use a list?
    def get_rating_before(self, season: int, round_number: int) -> Rating:
        current_season = self._ratings.get(season, {})
        rounds_before = [r for r in current_season.keys() if r < round_number]
        if rounds_before:
            return current_season[max(rounds_before)]

        seasons_before = [s for s in self._ratings.keys() if s < season]
        previous_season = self._ratings[max(seasons_before)]
        return previous_season[max(previous_season.keys())]

    def get_rating_on(self, season: int, iteration: int) -> Rating:
        return self._ratings[season][iteration]

    @property
    def rating(self) -> Rating:
        season_num = max(self._ratings.keys())
        current_season = self._ratings[season_num]
        round_num = max(current_season.keys())
        return current_season[round_num]

    @property
    def history(self) -> Iterator[Tuple[int, int, float, float]]:
        for season, rounds in self._ratings.items():
            for round_num, (mean, variance) in rounds.items():
                yield (season, round_num, mean, variance)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if not isinstance(other, Team):
            return NotImplemented
        return self.name == other.name

    def __repr__(self) -> str:
        try:
            rating = self.rating
        except ValueError:
            return f'Team(name={self._name}, rating=NA)'
        return f'Team(name={self._name}, rating={rating})'

    def __str__(self) -> str:
        return self.__repr__()

    def play_games(self, games):
        for game in games:
            self.games[game.season].append(game)

    def reset(self):
        # TODO: maybe don't put gross logic in here instead?
        self.games = defaultdict(list)
        self._ratings: Dict[int, Dict[int, Rating]] = {}

    def get_group(self, season: int) -> Optional[str]:
        """
        Look up the name of the group for a team in a particular season.
        None if the team didn't play in that season
        """
        if self._groups is None:
            return 'default'
        return self._groups.get(season)
