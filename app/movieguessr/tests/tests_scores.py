''' Score Tests '''

from datetime import datetime, timedelta
from movieguessr.models import Game, Movie, UserGame
from django.contrib.auth.models import User
from django.db.models import Sum
from django.test import TestCase


class TotalScoreTestCase(TestCase):
    ''' Total Score Test '''
    def setUp(self):
        ''' Set Up '''
        # create new user
        user = User.objects.create_user(username="Bilbo", password='123456')
        # add 2 movies
        movie = Movie(title="Fight Club", image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
        genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
        tagline="How much can you know about yourself if you've never been in a fight?",
        summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. \
            Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an \
                out-of-control spiral toward oblivion.")
        movie.save()
        movie1 = Movie(title="Fight Club 2", image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
        genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
        tagline="How much can you know about yourself if you've never been in a fight?",
        summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. \
            Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an \
                out-of-control spiral toward oblivion.")
        movie1.save()
        # add 2 games
        game = Game(movie=movie, date='2022-03-28')
        game.save()
        game1 = Game(movie=movie1, date='2022-03-27')
        game1.save()
        # add 2 results of score 600 and 400
        results = UserGame(user=user, game = game, tries=1, score=600)
        results.save()
        results1 = UserGame(user=user, game = game1, tries=2, score=400)
        results1.save()

    def test_total_score(self):
        ''' Add all scores for a User '''
        # get the User primary key
        user = User.objects.get(username="Bilbo").id
        # get total score for that user
        totalscore = UserGame.objects.filter(user=user).aggregate(Sum('score'))['score__sum']
        # should be equal to 1000
        self.assertEqual(totalscore, 1000)


class PreviousTotalScoreTestCase(TestCase):
    ''' Find Previous Total Score Test '''
    def setUp(self):
        ''' Set Up: create user, games, results '''
        # create new user
        user = User.objects.create_user(username="Bilbo", password='123456')
        # add 2 movies
        movie = Movie(title="Fight Club", image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
        genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
        tagline="How much can you know about yourself if you've never been in a fight?",
        summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. \
            Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an \
                out-of-control spiral toward oblivion.")
        movie.save()
        movie1 = Movie(title="Fight Club 2", image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
        genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
        tagline="How much can you know about yourself if you've never been in a fight?",
        summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. \
            Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an \
                out-of-control spiral toward oblivion.")
        movie1.save()
        # add 2 games
        game = Game(movie=movie, date=datetime.today().strftime('%Y-%m-%d'))
        game.save()
        date = datetime.today() - timedelta(days=1)
        game1 = Game(movie=movie1, date=date.strftime('%Y-%m-%d'))
        game1.save()
        # add 2 results of score 600 and 400
        results = UserGame(user=user, game = game, tries=1, score=600)
        results.save()
        results1 = UserGame(user=user, game = game1, tries=3, score=200)
        results1.save()

    def test_previous_total_score(self):
        ''' Test '''
        # get the User primary key
        user = User.objects.get(username="Bilbo").id
        # get total score for that user
        totalscore = UserGame.objects.filter(user=user).aggregate(Sum('score'))['score__sum']
        # should be equal to 1000
        self.assertEqual(totalscore, 800)
