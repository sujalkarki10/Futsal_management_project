# matchmaking/models.py
import datetime
from time import timezone
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from team.models import Team
#from venues.models import Venue

class Match(models.Model):
    MATCH_TYPE_CHOICES = [
        ('friendly', 'Friendly'),
        ('competitive', 'Competitive')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]

    team_a = models.ForeignKey(Team, related_name='matches_as_a', on_delete=models.CASCADE,null= True, blank=True)
    team_b = models.ForeignKey(Team, related_name='matches_as_b', on_delete=models.CASCADE, null=True, blank=True)
    mode = models.CharField(max_length=20, choices=MATCH_TYPE_CHOICES)
    #venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.team_a} vs {self.team_b or 'TBD'} ({self.mode})"

'''class Team(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="matchmaking_owned_teams")
    ranking = models.IntegerField(default=1000)  # ELO base rating
    status = models.CharField(max_length=20, default="available")

    wins = models.IntegerField(default=0)            # ✅ NEW
    matches_played = models.IntegerField(default=0)  # ✅ NEW


    def __str__(self):
        return self.name

'''

class MatchRequest(models.Model):
    MATCH_MODES = [
        ('friendly', 'Friendly'),
    ]

    team_a = models.ForeignKey(Team, related_name='sent_requests', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='received_requests', on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=MATCH_MODES, default='friendly')
    status = models.CharField(max_length=20,
    choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

