from django.db import models

class Game(models.Model):
    # ID might be a day?
    date = models.DateField('game date')

class Question(models.Model):
    # Order?
    # game = models.ForeignKey(Game, on_delete=models.CASCADE)
    movie_image_url = models.CharField(max_length=200)
    answer = models.CharField(max_length=200) # Might be a list of answers if we allow multiple

class GameQuestions(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

# Test script:
# python3 manage.py shell
# from movieguessr.models import Game, Question, GameQuestions
# q = Question(movie_image_url="https://occ-0-1722-1723.1.nflxso.net/dnm/api/v6/E8vDc_W8CLv7-yMQu8KMEC7Rrr8/AAAABdlE8rhGaCatmv2uA6l0WQMZu-bjDrxl97OWAt4s6RxTwl76ERcJ4VdoU6Fw8hSOpknhnROCQw1shVl6rm3qRhynqzer.jpg?r=b1b", answer = "Fight Club")

# Separate class for player instanced game for keeping track?