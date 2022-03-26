from django.db import models
# from urllib import request ??
from django.contrib.auth.models import User
from .movie import Movie

class Game(models.Model):
    date = models.DateField('game date')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title