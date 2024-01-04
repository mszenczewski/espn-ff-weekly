from typing import Optional
import configparser

from generate_report import generate_report

CONFIG = configparser.RawConfigParser()
CONFIG.read(r'config.txt')


def get_config(header: str, key: str, return_type: Optional[type] = str):
    value = CONFIG.get(header, key)
    if return_type is str:
        return str(value)
    if return_type is int:
        return int(value)
    if return_type is bool:
        if str.lower(value) == 'false':
            return False
        return True
    if return_type is list:
        value = value.replace('[', '')
        value = value.replace(']', '')
        value = value.replace(',', '')
        return str.split(value)
    raise ValueError('invalid config type')


ESPN_S2 = get_config('LEAGUE', 'espn_s2')
SWID = get_config('LEAGUE', 'swid')
LEAGUE_ID = get_config('LEAGUE', 'league_id', int)
YEARS = get_config('LEAGUE', 'years', list)
NUM_WEEKS = get_config('LEAGUE', 'num_weeks', list)

SHOW_PAYOUTS = get_config('REPORT', 'show_payouts', bool)
SHOW_WEEKLY = get_config('REPORT', 'show_weekly', bool)
WEEKLY_THRESHOLD = get_config('REPORT', 'weekly_threshold', int)

OUTPUT_FILE = open('report.txt', 'w')

for i, YEAR in enumerate(YEARS):
    num_weeks = int(NUM_WEEKS[i])
    year = int(YEAR)
    report = generate_report(
        league_id=LEAGUE_ID,
        espn_s2=ESPN_S2,
        swid=SWID,
        num_weeks=num_weeks,
        year=year,
        show_payouts=SHOW_PAYOUTS,
        show_weekly=SHOW_WEEKLY,
        weekly_threshold=WEEKLY_THRESHOLD,
    )

    OUTPUT_FILE.write(report)
