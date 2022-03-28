'''User Game model'''

from django.db import models
from django.contrib.auth.models import User
from .game import Game

class UserGame(models.Model):
    '''UserGame model'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tries = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        '''Default string representation'''
        return f'{self.user.username} {self.game}'
