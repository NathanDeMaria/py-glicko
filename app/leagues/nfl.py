import os

from glicko import LeagueBuilder, read_csv, Parameter


LEAGUE_DIR = os.path.dirname(os.path.abspath(__file__))
LEAGUE = 'nfl'
CSV_PATH = os.path.join(LEAGUE_DIR, f'{LEAGUE}.csv')
PARAM_PATH = os.path.join(LEAGUE_DIR, f'{LEAGUE}.json')

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
if os.path.exists(PARAM_PATH):
    builder.load_parameters(PARAM_PATH)


if __name__ == '__main__':
    print(builder.optimize()[0])
    builder.save_parameters(PARAM_PATH)
