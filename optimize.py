import sys
import numpy as np
from scipy.optimize import minimize

from glicko import read_csv, run_league


def main(path):
    league = read_csv(path)
    best = float('inf'), None
    for i in range(1, 5):
        result = minimize(
            lambda iv: run_league(league, *iv, n_iterations=i)[0],
            x0=np.array([10000, 20000]),
            options=dict(disp=True)
        )
        discrepancy, _ = run_league(league, *result.x, n_iterations=i)
        print(discrepancy, result.x)
        if discrepancy < best[0]:
            best = discrepancy, result.x
    print(best)


if __name__ == '__main__':
    main(sys.argv[1])
