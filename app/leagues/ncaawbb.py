import os

from glicko import LeagueBuilder, read_csv


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ncaawbb.csv'
)

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [54000., 30000.]
)


if __name__ == '__main__':
    print(builder.optimize())
