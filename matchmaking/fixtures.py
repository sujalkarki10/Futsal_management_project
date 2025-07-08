# matchmaking/fixtures.py
from team.models import Team
from matchmaking.models import Match
from datetime import timedelta, date


def generate_round_robin(start_date=None):
    if start_date is None:
        start_date = date.today()

    teams = list(Team.objects.all())
    if len(teams) % 2 != 0:
        teams.append(None)  # dummy team for bye

    num_teams = len(teams)
    rounds = num_teams - 1
    matches_per_round = num_teams // 2
    schedule = []

    for round_num in range(rounds):
        round_matches = []
        for i in range(matches_per_round):
            team_a = teams[i]
            team_b = teams[num_teams - 1 - i]
            if team_a is not None and team_b is not None:
                match_date = start_date + timedelta(days=round_num)
                match = Match.objects.create(
                    team_a=team_a,
                    team_b=team_b,
                    mode="competitive",
                    scheduled_date=match_date
                )
                schedule.append(match)
        # rotate teams
        teams.insert(1, teams.pop())

    return schedule
