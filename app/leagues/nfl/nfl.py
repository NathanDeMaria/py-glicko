import os

from glicko import LeagueBuilder, read_csv, Parameter
from glicko.score import scaled_mov_builder


LEAGUE_DIR = os.path.dirname(os.path.abspath(__file__))
LEAGUE = 'nfl'
CSV_PATH = os.path.join(LEAGUE_DIR, f'{LEAGUE}.csv')
PARAMS_FILE = os.path.join(LEAGUE_DIR, f'{LEAGUE}.json')

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [
        Parameter(
            name='init_variance',
            value=11314.210465759572,
            bounds=[1.0, 1e5],
        ),
        Parameter(
            name='variance_over_time',
            value=13438.058369333827,
            bounds=[1.0, 1e5]
        )
    ],
    score_function_builder=scaled_mov_builder
)
if os.path.exists(PARAMS_FILE):
    builder.load_parameters(PARAMS_FILE)


if __name__ == '__main__':
    print(builder.optimize()[0])
    builder.save_parameters(PARAMS_FILE)
