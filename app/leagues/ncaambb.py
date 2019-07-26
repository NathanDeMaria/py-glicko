import os

from glicko import LeagueBuilder, read_csv, Parameter


CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ncaambb.csv'
)

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [
        Parameter(
            name='init_variance',
            value=54371.69206368768,
            bounds=[1.0, 1e5],
        ),
        Parameter(
            name='variance_over_time',
            value=29815.254590976412,
            bounds=[1.0, 1e5]
        )
    ]
)


if __name__ == '__main__':
    print(builder.optimize()[0])
