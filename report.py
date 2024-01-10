from typing import Optional, Union
from tabulate import tabulate
from itertools import chain
from espn_api.espn_api.football import League, Team


def __top_scorers(teams: list[Team], num_weeks: int) -> list[dict]:
    top_scorers = []

    for i in range(num_weeks):
        high_score = 0
        name = None

        for team in teams:
            score = team.scores[i]
            if score > high_score:
                high_score = score
                name = f"{team.owners[0]['firstName']} {team.owners[0]['lastName']}"

        top_scorers.append({
            'score': high_score,
            'name': name
        })

    return top_scorers


def __weekly_payouts(teams: list[Team], num_weeks: int) -> dict:
    payouts = {}

    for team in teams:
        name = f"{team.owners[0]['firstName']} {team.owners[0]['lastName']}"
        payouts[name] = 0

    top_scorers = __top_scorers(teams, num_weeks)

    for top_scorer in top_scorers:
        name = top_scorer['name']
        payouts[name] += 1

    sorted_payouts = sorted(payouts.items(), key=lambda item: item[1])
    sorted_payouts.reverse()

    return dict(sorted_payouts)


def __format_weekly_payouts(weekly_payouts: list[dict]) -> list[list]:
    return __format_data(weekly_payouts)


def __format_top_scorers(top_scorers: list[list], weekly_threshold: int) -> list[list]:
    for ts in top_scorers:
        ts[:] = [x for x in ts if x['score'] > weekly_threshold]
    top_scorers = __format_data(top_scorers)
    return top_scorers


def __format_data(data: Union[list, dict]) -> list[list]:
    max_len = max(len(d) for d in data)

    for i, d in enumerate(data):
        if type(d) is dict:
            data[i] = [x for x in d.items()]
        elif type(d) is list:
            data[i] = [(x['name'], x['score']) for x in d]
        else:
            raise ValueError

        padding = max_len - len(d)
        while padding != 0:
            data[i].append(('', ''))
            padding -= 1

    data = list(zip(*data))

    for i, d in enumerate(data):
        data[i] = list(chain.from_iterable(data[i]))

    return data


def generate_report(
        leagues: list[League],
        show_payouts: Optional[bool] = True,
        show_weekly: Optional[bool] = True,
        weekly_threshold: Optional[int] = 0
) -> str:
    report = ''

    weekly_payouts = []
    top_scorers = []
    years = []

    for league in leagues:
        teams = league.teams
        year = league.year
        num_weeks = len(league.settings.matchup_periods)
        wp = __weekly_payouts(teams, num_weeks)
        ts = __top_scorers(teams, num_weeks)

        weekly_payouts.append(wp)
        top_scorers.append(ts)

        years.append(str(year))
        years.append('')

    if show_payouts:
        weekly_payouts = __format_weekly_payouts(weekly_payouts)
        report += tabulate(weekly_payouts, headers=years)
        report = report.replace('--  --', '------')
        if show_weekly:
            report += '\n\n'

    if show_weekly:
        top_scorers = __format_top_scorers(top_scorers, weekly_threshold)
        report += tabulate(top_scorers, headers=years)
        report = report.replace('--  ------', '----------')

    return report
