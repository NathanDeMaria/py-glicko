import os

from glicko import LeagueBuilder, read_csv, Parameter


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'nfl.csv'
)

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [
        Parameter(
            name='init_variance',
            value=20532.046258449554,
            bounds=[1.0, 1e5],
        ),
        Parameter(
            name='variance_over_time',
            value=18432.791531085968,
            bounds=[1.0, 1e5]
        )
    ]
)


if __name__ == '__main__':
    print(builder.optimize()[0])
