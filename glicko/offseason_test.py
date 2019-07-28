import datetime
from unittest import TestCase

from .game import Game
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
        games = [Game(teams[0], teams[1], 1, 2, 0, 0, datetime.datetime.now())]
        league = League(teams=teams, games=games)
        RUN_OFFSEASON_GROUPED(league, 0)
        teams[0].update_rating((team_mean, 4), 0, 1)

        RUN_OFFSEASON_GROUPED(league, 1)
        # Make sure teams[1] takes the average from teams[0]
        self.assertEqual(teams[1].rating[0], team_mean)

    def test_grouped_runner_skip_season(self):
        team_mean = 123.
        teams = [
            Team('t1', groups={0: 'A', 1: 'A', 2: 'A'}),
            Team('t2', groups={2: 'A'})
        ]
        games = [Game(teams[0], teams[1], 1, 2, 0, 0, datetime.datetime.now())]
        league = League(teams=teams, games=games)
        RUN_OFFSEASON_GROUPED(league, 0)
        teams[0].update_rating((team_mean, 4), 0, 1)

        # Make sure teams[1] takes the average from teams[0]
        # but only after the 2nd offseason
        RUN_OFFSEASON_GROUPED(league, 1)
        with self.assertRaises(ValueError):
            _ = teams[1].rating[0]
        RUN_OFFSEASON_GROUPED(league, 2)

        self.assertEqual(teams[1].rating[0], team_mean)

    def test_grouped_runner__new_group_middle(self):
        team_mean = 123.
        teams = [
            Team('t1', groups={0: 'A', 1: 'A'}),
            Team('t2', groups={1: 'B'}),
            Team('t3', groups={0: 'C', 1: 'C'}),
            Team('t4', groups={0: 'D', 1: 'D'}),
        ]
        games = [Game(teams[0], teams[1], 1, 2, 0, 0, datetime.datetime.now())]
        league = League(teams=teams, games=games)
        RUN_OFFSEASON_GROUPED(league, 0)
        teams[0].update_rating((team_mean / 2, 4), 0, 1)
        teams[2].update_rating((team_mean * 3 / 2, 4), 0, 1)
        teams[3].update_rating((team_mean * 10, 4), 0, 1)

        RUN_OFFSEASON_GROUPED(league, 1)
        # Make sure teams[1] takes the average from teams[0] and teams[2]
        self.assertEqual(teams[1].rating[0], team_mean)

    def test_grouped_runner__new_group_start(self):
        team_mean = 123.
        teams = [
            Team('t2', groups={1: 'A'}),
            Team('t1', groups={0: 'B', 1: 'B'}),
            Team('t3', groups={0: 'C', 1: 'C'}),
            Team('t4', groups={0: 'D', 1: 'D'}),
        ]
        games = [Game(teams[0], teams[1], 1, 2, 0, 0, datetime.datetime.now())]
        league = League(teams=teams, games=games)
        RUN_OFFSEASON_GROUPED(league, 0)
        teams[1].update_rating((team_mean, 4), 0, 1)
        teams[2].update_rating((team_mean * 10, 4), 0, 1)
        teams[3].update_rating((team_mean * 10, 4), 0, 1)

        RUN_OFFSEASON_GROUPED(league, 1)
        # Make sure teams[0] takes the average from teams[1]
        self.assertEqual(teams[0].rating[0], team_mean)

    def test_grouped_runner__new_group_end(self):
        team_mean = 123.
        teams = [
            Team('t1', groups={0: 'A', 1: 'A'}),
            Team('t4', groups={0: 'B', 1: 'B'}),
            Team('t3', groups={0: 'C', 1: 'C'}),
            Team('t2', groups={1: 'D'}),
        ]
        games = [Game(teams[0], teams[1], 1, 2, 0, 0, datetime.datetime.now())]
        league = League(teams=teams, games=games)
        RUN_OFFSEASON_GROUPED(league, 0)
        teams[0].update_rating((team_mean * 10, 4), 0, 1)
        teams[1].update_rating((team_mean * 10, 4), 0, 1)
        teams[2].update_rating((team_mean, 4), 0, 1)

        RUN_OFFSEASON_GROUPED(league, 1)
        # Make sure teams[3] takes the average from teams[2]
        self.assertEqual(teams[3].rating[0], team_mean)
