from typing import Optional
from espn_api.espn_api.football import League
import configparser

CFG_HEADER = 'default'
with open(r'config.txt') as cfg:
    config = configparser.RawConfigParser()
    config.read_string(f"[{CFG_HEADER}]\n" + cfg.read())


def get_config(key: str, return_type: Optional[type] = str):
    value = config.get(CFG_HEADER, key)
    if return_type is int:
        return int(value)
    return str(value)


NUM_WEEKS = get_config('num_weeks', int)
ESPN_S2 = get_config('espn_s2')
SWID = get_config('swid')
YEAR = get_config('year', int)
LEAGUE_ID = get_config('league_id', int)

league = League(
    league_id=LEAGUE_ID,
    year=YEAR,
    espn_s2=ESPN_S2,
    swid=SWID
)

teams = league.teams
payouts = {}
top_scorers = []

for team in teams:
    name = f"{team.owners[0]['firstName']} {team.owners[0]['lastName']}"
    payouts[name] = 0

for i in range(NUM_WEEKS):
    high_score = 0
    winner = None
    name = None

    for team in teams:
        if team.scores[i] > high_score:
            high_score = team.scores[i]
            name = f"{team.owners[0]['firstName']} {team.owners[0]['lastName']}"

    top_scorers.append({
        'score': high_score,
        'name': name
    })

    payouts[name] = payouts[name] + 1

for i, top_scorer in enumerate(top_scorers):
    week = i + 1
    name = top_scorer['name']
    score = top_scorer['score']
    print(f"Week {week:2}: {name:20} {score}")

print()

for name in payouts:
    print(f"{name:18} {payouts[name]}")
