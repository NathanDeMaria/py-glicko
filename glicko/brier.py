import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss

from .update import calc_win_prob
from .league import League


def calc_brier_score(league: League) -> float:
    result_array = _create_result_array(league)
    return brier_score_loss(result_array[:, 1], result_array[:, 0])


def create_calibration_curve(
        league: League,
        n_bins: int = 10
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns
    -------
    true
        Actual true proportions in each bin.
    predicted
        Expected true proportion in each bin.
    """
    x = _create_result_array(league)
    return calibration_curve(x[:, 1], x[:, 0], n_bins=n_bins)


def _create_result_array(league: League) -> np.ndarray:
    """
    :returns: array of shape (n, 3), where the columns represent:
        - Win probability
        - 1 for win, 0 for loss
        - Score of the game (scaled to s0-1)
    """
    results: List[Tuple] = []
    for g in league.games:
        game_day = g.season, g.round
        team_rating = g.team.get_rating_before(*game_day)
        away_rating = g.opponent.get_rating_before(*game_day)
        win_prob = calc_win_prob(team_rating, away_rating)
        win = g.team_score > g.opponent_score
        results.append((win_prob, win, g.score))
    return np.array(results)


def plot_calibration_curve(league: League):
    brier = calc_brier_score(league)
    true, predicted = create_calibration_curve(league)
    plt.plot(predicted, true)
    plt.xlabel("Expected %")
    plt.ylabel("Observed %")
    plt.title(f"Brier score: {brier:.03f}")
    plt.plot([0, 1], [0, 1])
