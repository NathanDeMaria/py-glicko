import os
import pandas as pd

from glicko import LeagueBuilder, read_csv

parent_dir = os.path.dirname(os.path.abspath(__file__))
conferences_path = os.path.join(parent_dir, 'ncaaf_conferences.csv')

CSV_PATH = os.path.join(parent_dir, 'ncaaf.csv')

fbs_conferences = {
    # Power 5
    1, 4, 5, 8, 9,
    # Group of 5
    12, 15, 151, 17, 37,
    # Independent
    18,
}

conferences = pd.read_csv(conferences_path)
fbs_lookup = {
    row.team: (row.team_conf in fbs_conferences)
    for _, row in conferences.iterrows()
}


def is_fbs(team_name: str) -> bool:
    return fbs_lookup[team_name]


def create_offseason_runner(
    init_variance: float,
    variance_over_time: float,
    fbs_advantage: float,
):
    def run_offseason(l, season: int) -> None:
        for team in l.teams:
            try:
                mean, var = team.rating
                team.update_rating(
                    (mean, var + variance_over_time),
                    season,
                    0
                )
            except ValueError:
                # i.e. this was the first season.
                multiplier = .5 if is_fbs(team.name) else -.5
                team.update_rating(
                    (1500 + fbs_advantage * multiplier, init_variance),
                    season,
                    0
                )
    return run_offseason


league = read_csv(CSV_PATH)
builder = LeagueBuilder(
    league,
    [132651.43369133995, 23133.307212227475, 578.8213423010113],
    offseason_runner_builder=create_offseason_runner,
)


if __name__ == '__main__':
    print(builder.optimize())
