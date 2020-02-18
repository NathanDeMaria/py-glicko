import os

from glicko import LeagueBuilder, read_csv, Parameter


LEAGUE_DIR = os.path.dirname(os.path.abspath(__file__))
LEAGUE = 'ncaawbb'
CSV_PATH = os.path.join(LEAGUE_DIR, f'{LEAGUE}.csv')
PARAMS_FILE = os.path.join(LEAGUE_DIR, f'{LEAGUE}.json')

league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [
        Parameter(
            name='init_variance',
            value=70671.7849420808,
            bounds=[1.0, 1e5],
        ),
        Parameter(
            name='variance_over_time',
            value=30205.62250227284,
            bounds=[1.0, 1e5]
        )
    ]
)
if os.path.exists(PARAMS_FILE):
    builder.load_parameters(PARAMS_FILE)


if __name__ == '__main__':
    print(builder.optimize(total_trials=50)[0])
    builder.save_parameters(PARAMS_FILE)
