from typing import Optional
from espn_api.espn_api.football import League


def generate_report(
        league_id,
        espn_s2,
        swid,
        num_weeks,
        year,
        show_payouts: Optional[bool] = True,
        show_weekly: Optional[bool] = True,
        weekly_threshold: Optional[int] = 0
):
    league = League(
        league_id=league_id,
        year=year,
        espn_s2=espn_s2,
        swid=swid
    )

    teams = league.teams
    payouts = {}
    top_scorers = []

    for team in teams:
        name = f"{team.owners[0]['firstName']} {team.owners[0]['lastName']}"
        payouts[name] = 0

    for i in range(num_weeks):
        high_score = 0
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

    print(f"{year}\n----")
    if show_weekly:
        for i, top_scorer in enumerate(top_scorers):
            week = i + 1
            name = top_scorer['name']
            score = top_scorer['score']
            if score >= weekly_threshold:
                print(f"Week {week:2}: {name:20} {score}")

        print()

    if show_payouts:
        for name in payouts:
            print(f"{name:18} {payouts[name]}")
