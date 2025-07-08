from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Team(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=50, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE,related_name="managed_teams") #Each Team is linked to its manager (a User,suppose sujal )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Meta:
    unique_together= ("name", "manager")

class Player(models.Model):
    POSITION_CHOICES = [
        ('Goalkeeper', 'Goalkeeper'),
        ('Defender', 'Defender'),
        ('Midfielder', 'Midfielder'),
        ('Forward', 'Forward')
    ]

    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='player_photos/', blank=True, null=True)
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        return self.name
