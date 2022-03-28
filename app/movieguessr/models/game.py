'''Game model'''

from django.db import models
from .movie import Movie

class Game(models.Model):
    '''Game model'''
    date = models.CharField(max_length=50, unique=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        '''Model stirng representation.'''
        return self.movie.title
