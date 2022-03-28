from datetime import datetime, timedelta
from django.test import TestCase
from movieguessr.models import Game, Movie

class GameTests(TestCase):
    def setUp(self):
        '''This method setups the tests.'''
        Movie.objects.create(
            title="Fight Club", 
            image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
            genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
            tagline="How much can you know about yourself if you've never been in a fight?",
            summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.")

    def test_game_not_today(self):
        '''Test to see if game is not today'''
        movie = Movie.objects.get(name="Fight Club")
        date = datetime.now() - timedelta(days=2)
        game = Game(movie=movie, date=date.strftime('%Y-%m-%d'))
        self.assertIs(game.is_game_today(), False)
   
    def test_game_is_today(self):
        '''Test to see if game is today'''
        movie = Movie.objects.get(name="Fight Club")
        game = Game(movie=movie, date=datetime.now().strftime('%Y-%m-%d'))
        self.assertIs(game.is_game_today(), True)
