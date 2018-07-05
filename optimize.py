import sys
import numpy as np
from scipy.optimize import minimize

from glicko import run_league, read_csv


def main(path):
    league = read_csv(path)
    result = minimize(
        lambda iv: run_league(league, *iv)[0],
        x0=np.array([41813.3907686, 63652.58824019]),
        options=dict(disp=True)
    )
    print(result.x)


if __name__ == '__main__':
    main(sys.argv[1])
