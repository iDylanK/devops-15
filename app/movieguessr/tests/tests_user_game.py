'''Module for the UserGame object tests.'''
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from movieguessr.models import UserGame, Movie, Game

class UserGameModelTests(TestCase):
    '''Class that holds all the UserGameModelTests.'''

    def setUp(self):
        '''Method that configures the necessary objects for the UserGame tests.'''
        User.objects.create(username="Filippo", password='123456')
        movie = Movie.objects.create(
            title="Spider-Man: No Way Home",
            image_url="https://image.tmdb.org/t/p/original/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
            genres="Action, Adventure, Science Fiction", release_date="2021-12-15", actor="Tom Holland", character="Peter Parker / Spider-Man",
            tagline="The Multiverse unleashed.",
            summary="Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero. " +
            "When he asks for help from Doctor Strange the stakes become even more dangerous, " +
            "forcing him to discover what it truly means to be Spider-Man.")
        Game.objects.create(movie=movie, date=datetime.today().strftime('%Y-%m-%d'))

    def test_user_can_play(self):
        '''Method to test whether a user can play a game. This method uses the UserGame object method `can_user_play`.'''
        user = User.objects.get(username="Filippo").id
        todays_game = Game.objects.get(date=datetime.today().strftime('%Y-%m-%d'))
        user_game = UserGame.objects.filter(user=user, game=todays_game.id).first()
        self.assertIsNone(user_game)

    def test_user_started_game_but_can_still_play(self):
        '''
        Method to test whether a user can still play a game despite having started it.
        This method uses the UserGame object method `can_user_play`.
        '''
        user = User.objects.get(username="Filippo")
        game = Game.objects.get(date=datetime.today().strftime('%Y-%m-%d'))
        user_game = UserGame.objects.create(user=user, game=game, tries=0, score=0)
        self.assertIs(user_game.can_user_play(), True)

    def test_user_cannot_play(self):
        '''Method to test a user cannot play a game after having used all the tries. This method uses the UserGame object method `can_user_play`.'''
        user = User.objects.get(username="Filippo")
        game = Game.objects.get(date=datetime.today().strftime('%Y-%m-%d'))
        user_game = UserGame.objects.create(user=user, game=game, tries=6, score=0)
        self.assertIs(user_game.can_user_play(), False)
