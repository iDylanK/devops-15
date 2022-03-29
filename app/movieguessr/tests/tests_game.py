'''Module that encompases all Game related tests specific to the Game object.'''
from datetime import datetime, timedelta
from django.test import TestCase
from movieguessr.models import Game, Movie

class GameTests(TestCase):
    '''A class to represent the GameTests.'''

    def setUp(self):
        '''Method that setups GameTests by creating the required Movie object.'''
        Movie.objects.create(
            title="The Adam Project",
            image_url="https://image.tmdb.org/t/p/original/wFjboE0aFZNbVOF05fzrka9Fqyx.jpg",
            genres="Action, Adventure, Comedy, Science Fiction, Drama", release_date="1999-10-15", actor="Ryan Reynolds", character="Adam Reed",
            tagline="Past meets future.",
            summary="After accidentally crash-landing in 2022, " +
            "time-traveling fighter pilot Adam Reed teams up with his 12-year-old self on a mission to save the future.")

    def test_game_not_today(self):
        '''Test to see if game is not today'''
        movie = Movie.objects.get(title="The Adam Project")
        date = datetime.now() - timedelta(days=2)
        game = Game(movie=movie, date=date.strftime('%Y-%m-%d'))
        self.assertIs(game.is_game_today(), False)

    def test_game_is_today(self):
        '''Test to see if game is today'''
        movie = Movie.objects.get(title="The Adam Project")
        game = Game(movie=movie, date=datetime.now().strftime('%Y-%m-%d'))
        self.assertIs(game.is_game_today(), True)
