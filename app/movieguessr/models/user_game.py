'''User Game model'''
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
from .game import Game

class UserGame(models.Model):
    '''UserGame model class.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    tries = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        '''Default string representation'''
        return f'{self.user.username} {self.game}'

    def can_user_play(self) -> Boolean:
        '''Returns whether a user can play the game based on if the number of tries are less than 6.'''
        return self.tries < 6
