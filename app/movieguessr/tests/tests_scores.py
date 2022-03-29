'''This module contains the scores tests.'''
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Sum
from movieguessr.models import Game, Movie, UserGame

class TotalScoreTestCase(TestCase):
    '''A class that tests whether scores are given correctly.'''

    def setUp(self):
        '''Method that set-ups objects for the total scores test.'''
        # create new user
        user = User.objects.create_user(username="Bilbo", password='123456')
        # add 2 movies
        movie = Movie.objects.create(
            title="Bridge of Spies",
            image_url="https://image.tmdb.org/t/p/original/bORlvwnVJE1Z6yIg96qnLLY3LJQ.jpg",
            genres="Drama", release_date="2015-10-15", actor="Tom Hanks", character="James B. Donovan",
            tagline="In the shadow of war, one man showed the world what we stood for.",
            summary="During the Cold War, the Soviet Union captures U.S. pilot Francis Gary Powers after shooting down his U-2 spy plane. " +
            "Sentenced to 10 years in prison, Powers' only hope is New York lawyer James Donovan, " +
            "recruited by a CIA operative to negotiate his release. " +
            "Donovan boards a plane to Berlin, hoping to win the young man's freedom through a prisoner exchange. " +
            "If all goes well, the Russians would get Rudolf Abel, the convicted spy who Donovan defended in court.")

        movie1 = Movie.objects.create(
            title="Fight Club 2",
            image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
            genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
            tagline="How much can you know about yourself if you've never been in a fight?",
            summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male " +
            "aggression into a shocking new form of therapy. " +
            "Their concept catches on, with underground \"fight clubs\" forming in every town, " +
            "until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.")

        # add 2 games
        date = datetime.today()
        date1 = date - timedelta(days=1)

        game = Game.objects.create(movie=movie, date=date.strftime('%Y-%m-%d'))
        game1 = Game.objects.create(movie=movie1, date=date1.strftime('%Y-%m-%d'))

        # add 2 results of score 600 and 400
        UserGame.objects.create(user=user, game = game, tries=1, score=600)
        UserGame.objects.create(user=user, game = game1, tries=2, score=400)

    def test_total_score(self):
        '''Method that set-ups objects for the total scores test.'''
        # get the User primary key.
        user = User.objects.get(username="Bilbo").id
        # get total score for that user
        totalscore = UserGame.objects.filter(user=user).aggregate(Sum('score'))['score__sum']
        # should be equal to 1000
        self.assertEqual(totalscore, 1000)

    def test_score_todays_game(self):
        '''Method checks the given score for todays game is correct.'''
        # get the User primary key
        user = User.objects.get(username="Bilbo").id
        # get todays game.
        todays_game = Game.objects.get(date=datetime.today().strftime('%Y-%m-%d'))
        # get score for that user for todays game.
        score = UserGame.objects.filter(user=user, game=todays_game.id).first().score
        # should be equal to 600
        self.assertEqual(score, 600)
