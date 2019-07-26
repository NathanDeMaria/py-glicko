import os

from glicko import LeagueBuilder, read_csv


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ncaambb.csv'
)

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [54371.69206368768, 29815.254590976412]
)


if __name__ == '__main__':
    print(builder.optimize())
