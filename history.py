import os
import sys
from csv import writer

from glicko import run_league, read_csv


def main(path: str):
    league = read_csv(path)
    _, teams = run_league(league, 41813.3907686, 63652.58824019)

    output_path = f'{os.path.splitext(os.path.basename(path))[0]}_history.csv'
    with open(output_path, 'w') as f:
        csv_writer = writer(f)
        csv_writer.writerow(['team', 'season', 'round', 'mean', 'variance'])
        for team in teams:
            for s, r, m, v in team.history:
                csv_writer.writerow([team.name, s, r, m, v])


if __name__ == '__main__':
    main(sys.argv[1])
