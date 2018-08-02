from datetime import datetime
from typing import List
from unittest import TestCase

from .backward import run_league
from .game import Game
from .league import League
from .team import Team


def _get_team(name: str, teams: List[Team]) -> Team:
    matches = [t for t in teams if t.name == name]
    if len(matches) != 1:
        ValueError("Stop, you dummy")
    return matches[0]


# TODO: better unit testable functions in backward.py
class TestBackward(TestCase):
    def test_backward__no_other_opponents(self):
        # If a team has only one opponent in a season, don't break.
        league = League([
            Game('a', 'b', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        discrepancy, teams = run_league(league, 100)

        self.assertGreater(discrepancy, 0)
        a = _get_team('a', teams)
        b = _get_team('b', teams)
        self.assertGreater(a.rating, b.rating)

    def test_backward__boost_from_backward(self):
        # You get a rating boost for beating somebody that beats somebody good,
        # even if your opponent gets that win after you play
        league = League([
            Game('a', 'b', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league, 100)

        a = _get_team('a', teams)

        league2 = League([
            Game('a', 'b', 1, 0, 1, 1, datetime(1976, 3, 24), 'A'),
            Game('b', 'c', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league2, 100)

        a2 = _get_team('a', teams)
        self.assertGreater(a2.rating, a.rating)

    def test_backward__no_opponents_opponents(self):
        # if n_iterations is 1, no boost from opponents' opponents
        league = League([
            Game('a', 'b', 1, 0, 1, 1, datetime.now(), 'A'),
            Game('b', 'c', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league, 100)

        a = _get_team('a', teams)

        league2 = League([
            Game('a', 'b', 1, 0, 1, 1, datetime(1976, 3, 24), 'A'),
            Game('b', 'c', 1, 0, 1, 1, datetime.now(), 'A'),
            # B gets a boost, but that doesn't make it to A
            Game('c', 'd', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league2, 100, n_iterations=1)

        a2 = _get_team('a', teams)
        self.assertEqual(a2.rating, a.rating)

    def test_backward__opponents_opponents(self):
        # if n_iterations is 1, no boost from opponents' opponents
        league = League([
            Game('a', 'b', 1, 0, 1, 1, datetime.now(), 'A'),
            Game('b', 'c', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league, 100)

        a = _get_team('a', teams)

        league2 = League([
            Game('a', 'b', 1, 0, 1, 1, datetime(1976, 3, 24), 'A'),
            Game('b', 'c', 1, 0, 1, 1, datetime.now(), 'A'),
            # B gets a boost, and that does make it to A
            Game('c', 'd', 1, 0, 1, 1, datetime.now(), 'A'),
        ])
        _, teams = run_league(league2, 100, n_iterations=2)

        a2 = _get_team('a', teams)
        self.assertGreater(a2.rating, a.rating)
