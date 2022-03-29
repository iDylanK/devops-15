'''Module to test views.'''
from django.test import TestCase

class ViewsTestCase(TestCase):
    '''Views tests class.'''

    def test_home_access(self):
        '''Method that determines whether accessing home returns a 200 code.'''
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_game_page_access(self):
        '''Method that determines whether accessing the game page returns a 200 code.'''
        response = self.client.get("/game/", follow=True)
        self.assertEqual(response.status_code, 200)
