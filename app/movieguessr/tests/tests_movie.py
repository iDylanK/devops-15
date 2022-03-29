'''Movie Model tests module.'''
from django.test import TestCase
from movieguessr.models import Movie

class MovieModelTests(TestCase):
    '''The MovieModelTests class to containing all movie object tests.'''

    def setUp(self):
        '''This method setups the movie model tests by creating a tester Interstellar movie object and adding it to the movies list.'''
        Movie.objects.create(
            title="Interstellar",
            image_url="https://image.tmdb.org/t/p/original/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            genres="Adventure, Drama, Science Fiction", release_date="2014-11-05", actor="Matthew McConaughey", character="Joseph 'Coop' Cooper",
            tagline="Mankind was born on Earth. It was never meant to die here.",
            summary="The adventures of a group of explorers who make use of a newly discovered wormhole " +
            "to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.")


    def test_movie_created_successfully(self):
        '''Test movie is created successfully'''
        movie = Movie.objects.get(title="Interstellar")
        self.assertEqual(movie.title, "Interstellar")

    def test_movie_retrieval_not_null(self):
        '''Test movie retrieved from all movies is not null'''
        movie = Movie.objects.get(title="Interstellar")
        self.assertIsNotNone(movie)

    def test_movie_retrieval_fail(self):
        '''Test to ensure that if searching for a movie doesn't exist null gets returned.'''
        with self.assertRaises(Movie.DoesNotExist):
            Movie.objects.get(title="A good year") # movie that doesn't exist for sure.
