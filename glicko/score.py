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
