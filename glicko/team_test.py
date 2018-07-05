from unittest import TestCase

from .team import Team


class TestTeam(TestCase):
    def test_team_rating__default(self):
        t = Team('Peyton')
        self.assertEqual((1500, 100), t.rating)

    def test_team_rating__multiple_seasons(self):
        t = Team('Peyton')
        high_rating = (9000, 1)
        t._ratings = {
            1: {1: (1500, 1), 2: (1600, 1)},
            2: {1: (1700, 1), 2: high_rating}
        }

        self.assertEqual(high_rating, t.rating)

    def test_team_get_rating_before__basic(self):
        t = Team('Peyton')
        t._ratings = {
            1: {1: (1500, 1), 2: (1600, 1)},
            2: {1: (1700, 1), 2: (9000, 1)}
        }

        rating = t.get_rating_before(2, 2)
        self.assertEqual((1700, 1), rating)

    def test_team_get_rating_before__previous_season(self):
        t = Team('Peyton')
        t._ratings = {
            1: {1: (1500, 1), 2: (1600, 1)},
            2: {1: (1700, 1), 2: (9000, 1)}
        }

        rating = t.get_rating_before(2, 1)
        self.assertEqual((1600, 1), rating)

    def test_team_get_rating_before__skipped_rounds(self):
        t = Team('Peyton')
        t._ratings = {
            1: {1: (1500, 1), 2: (1600, 1)},
            2: {1: (1700, 1), 4: (9000, 1)}
        }

        rating = t.get_rating_before(2, 3)
        self.assertEqual((1700, 1), rating)

    def test_team_get_rating_before__skipped_season(self):
        t = Team('Peyton')
        t._ratings = {
            1: {1: (1500, 1), 2: (1600, 1)},
            3: {1: (1700, 1), 4: (9000, 1)}
        }

        rating = t.get_rating_before(3, 1)
        self.assertEqual((1600, 1), rating)

    def test_team_get_rating_before__init_rating(self):
        t = Team('Peyton')
        t._ratings.update({
            1: {1: (1500, 1), 2: (1600, 1)},
            2: {1: (1700, 1), 4: (9000, 1)}
        })

        rating = t.get_rating_before(1, 1)
        self.assertEqual((1500, 100), rating)
