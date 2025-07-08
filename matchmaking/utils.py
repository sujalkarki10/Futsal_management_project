import math

def update_elo(winner, loser, k=32):
    def expected_score(r1, r2):
        return 1 / (1 + 10 ** ((r2 - r1) / 400))

    # Calculate expected scores
    winner_expected = expected_score(winner.ranking, loser.ranking)
    loser_expected = expected_score(loser.ranking, winner.ranking)

    # Update ELO ratings
    winner.ranking += round(k * (1 - winner_expected))
    loser.ranking += round(k * (0 - loser_expected))

    # Update match stats
    winner.wins += 1
    winner.matches_played += 1
    loser.matches_played += 1

    # Save all
    winner.save()
    loser.save()

import math
from datetime import timedelta, date
from team.models import Team
from matchmaking.models import Match

def compute_team_score(team):
    if team.matches_played == 0:
        return 0
    win_rate = team.wins / team.matches_played
    return win_rate * math.log(team.matches_played + 1)

def generate_smart_fixtures(start_date=None):
    if start_date is None:
        start_date = date.today()

    teams = list(Team.objects.all())
    teams = sorted(teams, key=lambda t: compute_team_score(t), reverse=True)

    # If odd number of teams, add None for BYE
    if len(teams) % 2 != 0:
        teams.append(None)

    match_date = start_date
    for i in range(0, len(teams), 2):
        team_a = teams[i]
        team_b = teams[i + 1]
        if team_a and team_b:
            Match.objects.create(
                team_a=team_a,
                team_b=team_b,
                mode='competitive',
                scheduled_date=match_date
            )
        match_date += timedelta(days=1)  # 1 match per team per day
