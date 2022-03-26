from django.db import models
# from urllib import request ??
from django.contrib.auth.models import User
from .game import Game

class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tries = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)
    total_score = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return f'{self.user.username} {self.game}'
    
