"""
Scoring functions: methods for evaluating a game's performance
as a value between [0, 1].
"""
import numpy as np
from typing import Callable
from scipy.stats import norm

from .game import Game
from .league import League


ScoreFunction = Callable[[Game], float]


def pwp(game: Game, exponent: float = 2.0) -> float:
    denom = (game.team_score ** exponent + game.opponent_score ** exponent)
    return (game.team_score ** exponent) / denom


def mov_cdf_builder(league: League) -> ScoreFunction:
    mov_std = np.std([g.team_score - g.opponent_score for g in league.games])
    mov_dist = norm(loc=0, scale=mov_std)

    def score(game):
        mov = game.team_score - game.opponent_score
        return mov_dist.cdf(mov)

    return score


def _hensley(game: Game) -> float:
    v = (min(game.team_score, game.opponent_score)
         / max(game.team_score, game.opponent_score))
    mov = game.team_score - game.opponent_score
    sign = np.sign(mov)
    return sign * np.sqrt((1 - v) * abs(mov))


def hensley_cdf_builder(league: League) -> ScoreFunction:
    hs = [_hensley(g) for g in league.games]
    mean = np.mean(hs)
    std = np.std(hs)
    dist = norm(loc=mean, scale=std)

    def score(game):
        h = _hensley(game)
        return dist.cdf(h)

    return score


def _scaled_mov(game: Game) -> float:
    # Inspired by fivethirtyeight's method for scaling margin of victory
    # https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/
    mov = game.team_score - game.opponent_score
    return np.sign(mov) * np.log(np.abs(mov) + 1) * 2.2 / (np.abs(mov) * .001 + 2.2)


def scaled_mov_builder(league: League) -> ScoreFunction:
    scaled_movs = [_scaled_mov(g) for g in league.games]
    min_mov, max_mov = min(scaled_movs), max(scaled_movs)
    # Assert that they're opposites, but leave room for rounding errors
    assert np.abs(min_mov + max_mov) < 1e-3

    def score(game: Game) -> float:
        s = _scaled_mov(game)
        return (s - min_mov) / (max_mov - min_mov)
    
    return score
