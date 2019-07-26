from typing import Tuple

import numpy as np

from .team import Rating


Q = np.log(10) / 400
EPSILON = 1e-16


def _g(variance: np.ndarray) -> np.ndarray:
    return 1 / np.sqrt(1 + 3 * (Q ** 2) * variance / (np.pi ** 2))


# TODO: figure out if I should do this on numpy arrays instead
def update_rating(rating: Rating,
                  opponent_results: np.ndarray) -> Tuple[Rating, float]:
    r"""

    :param rating: rating of the player
    :param opponent_results: ``(n, 3)`` array of means, variances, and scores.
    :return: updated player rating and discrepancy
    """
    if opponent_results.shape[0] == 0:
        return rating, 0
    team_mean, team_variance = rating
    opponent_means, opponent_variances, scores = opponent_results.T
    g_opp = _g(opponent_variances)
    mean_diff = (team_mean - opponent_means) / 400
    expected_scores = 1 / (1 + 10 ** (-g_opp * mean_diff))

    game_sums = ((g_opp ** 2) * expected_scores * (1 - expected_scores)).sum()
    # Plus epsilon to avoid div0
    delta_sq = 1 / ((Q ** 2) * game_sums + EPSILON)
    updated_variance = 1 / (1 / team_variance + 1 / delta_sq)
    weighted_surprise = (g_opp * (scores - expected_scores)).sum()
    update_mean = team_mean + Q * updated_variance * weighted_surprise

    win_prob = calc_win_prob(rating, opponent_results[..., :2].T)
    # To avoid log(0)
    win_prob = np.maximum(np.minimum(win_prob, 1 - EPSILON), EPSILON)
    discrepancies = (-scores * np.log(win_prob)
                     - (1 - scores) * np.log(1 - win_prob))

    return (update_mean, updated_variance), discrepancies.sum()


def calc_win_prob(team_rating, opponent_rating) -> float:
    team_mean, team_variance = team_rating
    opp_mean, opponent_variance = opponent_rating
    mean_diff = (team_mean - opp_mean) / 400
    g_combo = _g(team_variance + opponent_variance)
    return 1 / (1 + 10 ** (-g_combo * mean_diff))
