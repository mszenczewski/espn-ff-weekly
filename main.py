from generate_report import generate_report
from config import get_config

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
