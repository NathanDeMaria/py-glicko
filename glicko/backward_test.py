from datetime import datetime
from unittest import TestCase

from .backward import run_league
from .game import Game
from .league import League
from .team import Team


class TestBackward(TestCase):
    def test_backward__no_other_opponents(self):
        # If a team has only one opponent in a season, don't break.
        a, b = Team('a'), Team('b')
        league = League([
            Game(a, b, 1, 0, 1, 1, datetime.now()),
        ])
        discrepancy, _ = run_league(league, 100)

        self.assertGreater(discrepancy, 0)
        self.assertGreater(a.rating, b.rating)

    def test_backward__boost_from_backward(self):
        # You get a rating boost for beating somebody that beats somebody good,
        # even if your opponent gets that win after you play
        a, b = Team('a'), Team('b')
        league = League([
            Game(a, b, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league, 100)

        a2, b2, c2 = Team('a'), Team('b'), Team('c')
        league2 = League([
            Game(a2, b2, 1, 0, 1, 1, datetime(1976, 3, 24)),
            Game(b2, c2, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league2, 100)

        self.assertGreater(a2.rating, a.rating)

    def test_backward__no_opponents_opponents(self):
        # if n_iterations is 1, no boost from opponents' opponents
        a, b, c = Team('a'), Team('b'), Team('c')
        league = League([
            Game(a, b, 1, 0, 1, 1, datetime.now()),
            Game(b, c, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league, 100)

        a2, b2, c2, d2 = Team('a'), Team('b'), Team('c'), Team('d')
        league2 = League([
            Game(a2, b2, 1, 0, 1, 1, datetime(1976, 3, 24)),
            Game(b2, c2, 1, 0, 1, 1, datetime.now()),
            # B gets a boost, but that doesn't make it to A
            Game(c2, d2, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league2, 100, n_iterations=1)
        self.assertEqual(a2.rating, a.rating)

    def test_backward__opponents_opponents(self):
        # if n_iterations is 1, no boost from opponents' opponents
        a, b, c = Team('a'), Team('b'), Team('c')
        league = League([
            Game(a, b, 1, 0, 1, 1, datetime.now()),
            Game(b, c, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league, 100)

        a2, b2, c2, d2 = Team('a'), Team('b'), Team('c'), Team('d')
        league2 = League([
            Game(a2, b2, 1, 0, 1, 1, datetime(1976, 3, 24)),
            Game(b2, c2, 1, 0, 1, 1, datetime.now()),
            # B gets a boost, and that does make it to A
            Game(c2, d2, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league2, 100, n_iterations=2)

        self.assertGreater(a2.rating, a.rating)

    def test_backward__none_from_next_season(self):
        # You don't get a boost from beating
        # somebody with a big win next season
        a, b = Team('a'), Team('b')
        league = League([
            Game(a, b, 1, 0, 1, 1, datetime.now()),
        ])
        run_league(league, 100)

        a2, b2, c2 = Team('a'), Team('b'), Team('c')
        league2 = League([
            Game(a2, b2, 1, 0, 1, 1, datetime(1976, 3, 24)),
            Game(b2, c2, 1, 0, 2, 1, datetime.now()),
        ])
        run_league(league2, 100)

        self.assertEqual(a2.rating, a.rating)

    def test_backward__first_season_is_not_one(self):
        a, b = Team('a'), Team('b')
        league = League([
            Game(a, b, 1, 0, 1000, 1, datetime.now()),
        ])
        discrepancy, teams = run_league(league, 100)

        self.assertGreater(discrepancy, 0)
        self.assertGreater(a.rating, b.rating)