import numpy as np
from unittest import TestCase

from .update import update_rating


class TestUpdate(TestCase):
    def test_update_rating__equal_tie_drops_variance(self):
        # Same rating, tie -> lower variance
        (update_mean, updated_variance), _ = update_rating(
            (1500, 100),
            np.array([
                [1500, 100, 0.5],
            ])
        )
        self.assertEqual(1500, update_mean)
        self.assertLess(updated_variance, 100)

    def test_update_rating__equal_win_loss_is_a_wash(self):
        # win vs somebody better, loss vs somebody equally worse -> no change
        (update_mean, updated_variance), _ = update_rating(
            (1500, 100),
            np.array([
                [1600, 100, 1],
                [1400, 100, 0],
            ])
        )
        self.assertEqual(1500, update_mean)
        self.assertLess(updated_variance, 100)

    def test_update_rating__moral_victory_can_raise_rating(self):
        # If you were supposed to get crushed, but barely lost,
        # you're probably better than we thought you were
        (update_mean, updated_variance), _ = update_rating(
            (1500, 100),
            np.array([
                [2100, 100, 0.4],
            ])
        )
        self.assertGreater(update_mean, 1500)
        self.assertLess(updated_variance, 100)

    def test_update_rating__but_losing_is_still_bad(self):
        # If you were supposed to get crushed, but barely lost,
        # you're probably better than we thought you were
        (update_mean, updated_variance), _ = update_rating(
            (1500, 100),
            np.array([
                [1500, 100, 0.4],
            ])
        )
        self.assertLess(update_mean, 1500)
        self.assertLess(updated_variance, 100)
