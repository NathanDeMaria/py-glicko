import os

from glicko import LeagueBuilder, read_csv


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'nfl.csv'
)

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [10135.827483152862, 11418.89418889558]
)


if __name__ == '__main__':
    print(builder.optimize())
