import os

from generate_report import generate_report
from config import get_config
from espn_api.espn_api.football import League
import pickle
from os.path import exists

ESPN_S2 = get_config('LEAGUE', 'espn_s2')
SWID = get_config('LEAGUE', 'swid')
LEAGUE_ID = get_config('LEAGUE', 'league_id', int)
YEARS = get_config('LEAGUE', 'years', list)
NUM_WEEKS = get_config('LEAGUE', 'num_weeks', list)

SHOW_PAYOUTS = get_config('REPORT', 'show_payouts', bool)
SHOW_WEEKLY = get_config('REPORT', 'show_weekly', bool)
WEEKLY_THRESHOLD = get_config('REPORT', 'weekly_threshold', int)

OUTPUT_FILENAME = get_config('REPORT', 'output_filename')
OUTPUT_FILE = open(OUTPUT_FILENAME, 'w')


def main():
    for i, year in enumerate(YEARS):
        num_weeks = NUM_WEEKS[i]
        cached_league_filename = f".league_cache/{LEAGUE_ID}_{year}"

        if exists(cached_league_filename):
            with open(cached_league_filename, 'rb') as cached_league_file:
                league = pickle.load(cached_league_file)
        else:
            league = League(
                league_id=LEAGUE_ID,
                year=year,
                espn_s2=ESPN_S2,
                swid=SWID
            )

            if not exists('.league_cache'):
                os.mkdir('.league_cache')

            with open(cached_league_filename, 'wb+') as cached_league_file:
                pickle.dump(league, cached_league_file)

        report = generate_report(
            league=league,
            num_weeks=num_weeks,
            year=year,
            show_payouts=SHOW_PAYOUTS,
            show_weekly=SHOW_WEEKLY,
            weekly_threshold=WEEKLY_THRESHOLD,
        )

        OUTPUT_FILE.write(report)

    OUTPUT_FILE.close()


if __name__ == "__main__":
    main()
