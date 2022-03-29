from turtle import title
from unicodedata import name
from django.test import TestCase
from movieguessr.models import Movie

class MovieModelTests(TestCase):
    def setUp(self):
        '''This method setups the movie model tests by creating a tester Fight Club model'''
        Movie.objects.create(
            title="Fight Club", 
            image_url="https://image.tmdb.org/t/p/original/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
            genres="Drama", release_date="1999-10-15", actor="Brad Pitt", character="Edward Norton",
            tagline="How much can you know about yourself if you've never been in a fight?",
            summary="A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.")


    def test_movie_created_successfully(self):
        '''Test to see if movie is created successfully'''
        movie = Movie.objects.get(title="Fight Club")
        self.assertEqual(movie.title, "Fight Club")

    def test_movie_retrieval_not_null(self):
        '''Test to see if movie retrieved from all movies is not null'''
        movie = Movie.objects.get(title="Fight Club")
        self.assertIsNotNone(movie)

    def test_movie_retrieval_fail(self):
        '''Test to ensure that if searching for a movie doesn't exist null gets returned.'''
        with self.assertRaises(Movie.DoesNotExist):
            movie = Movie.objects.get(title="A good year") # movie that doesn't exist for sure.
