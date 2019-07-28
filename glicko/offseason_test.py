from unittest import TestCase

from .league import League
from .offseason import create_grouped_offseason_runner
from .team import Team


RUN_OFFSEASON_GROUPED = create_grouped_offseason_runner(10, 10)


class TestOffseason(TestCase):
    def test_grouped_runner(self):
        team_mean = 123.
        teams = [
            Team('t1', groups={0: 'A', 1: 'A'}),
            Team('t2', groups={1: 'A'})
        ]
        teams[0].update_rating((team_mean, 4), 0, 1)
        league = League(teams=teams, games=[])

        RUN_OFFSEASON_GROUPED(league, 1)
        # Make sure teams[1] takes the average from teams[0]
        self.assertEqual(teams[1].rating[0], team_mean)

    def test_grouped_runner_skip_season(self):
        team_mean = 123.
        teams = [
            Team('t1', groups={0: 'A', 1: 'A', 2: 'A'}),
            Team('t2', groups={2: 'A'})
        ]
        teams[0].update_rating((team_mean, 4), 0, 1)
        league = League(teams=teams, games=[])

        # Make sure teams[1] takes the average from teams[0]
        # but only after the 2nd offseason
        RUN_OFFSEASON_GROUPED(league, 1)
        with self.assertRaises(ValueError):
            _ = teams[1].rating[0]
        RUN_OFFSEASON_GROUPED(league, 2)

        self.assertEqual(teams[1].rating[0], team_mean)
