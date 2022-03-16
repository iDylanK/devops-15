from django.db import models
# from urllib import request ??
from django.contrib.auth.models import User

class Movies(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image_url = models.URLField()
    genres = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=20)
    actor = models.CharField(max_length=100)
    character = models.CharField(max_length=200)
    summary = models.TextField(null=True)

class GamesOfTheDay(models.Model):
    date = models.DateField('game date')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

class UserGames(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(GamesOfTheDay, on_delete=models.CASCADE)

    tries = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0)

# Test script:
# python3 manage.py shell
# from movieguessr.models import Movies, GamesOfTheDay, UserGames
# q = Question(movie_image_url="https://occ-0-1722-1723.1.nflxso.net/dnm/api/v6/E8vDc_W8CLv7-yMQu8KMEC7Rrr8/AAAABdlE8rhGaCatmv2uA6l0WQMZu-bjDrxl97OWAt4s6RxTwl76ERcJ4VdoU6Fw8hSOpknhnROCQw1shVl6rm3qRhynqzer.jpg?r=b1b", answer = "Fight Club")