from typing import Optional


def __top_scorers(teams, num_weeks) -> list:
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


def __weekly_payouts(teams, num_weeks) -> dict:
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


def generate_report(
        league,
        num_weeks,
        year,
        show_payouts: Optional[bool] = True,
        show_weekly: Optional[bool] = True,
        weekly_threshold: Optional[int] = 0
) -> str:
    report = ''
    teams = league.teams
    payouts = __weekly_payouts(teams, num_weeks)
    top_scorers = __top_scorers(teams, num_weeks)

    report += f"{year}\n----\n"
    if show_weekly:
        for i, top_scorer in enumerate(top_scorers):
            week = i + 1
            name = top_scorer['name']
            score = top_scorer['score']
            if score >= weekly_threshold:
                report += f"Week {week:2}: {name:20} {score}\n"
        report += '\n'

    if show_payouts:
        for name in payouts:
            report += f"{name:18} {payouts[name]}\n"
        report += '\n'

    return report
