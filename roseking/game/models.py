from django.contrib.auth.models import User
from django.db import models


class BrezelWars(models.Model):
    game_id = models.CharField(max_length=64)
    players = models.ManyToManyField(to=User)
    player_one_username = models.CharField(max_length=128)
    player_two_username = models.CharField(max_length=128)
    player_one_points = models.IntegerField()
    player_two_points = models.IntegerField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(auto_now=True)
    steps = models.CharField(max_length=1024)
