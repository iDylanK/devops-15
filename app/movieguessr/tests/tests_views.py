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
        response = self.client.get("/game/")
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_page_access(self):
        '''Method that determines whether accessing the leaderboard page returns a 200 code.'''
        response = self.client.get("/leaderboard/")
        self.assertEqual(response.status_code, 200)

    def test_admin_page_access(self):
        '''Method that determines whether accessing the admin page returns a code other than 200.'''
        response = self.client.get("/admin/")
        self.assertNotEqual(response.status_code, 200)

    def test_accounts_page_access(self):
        '''Method that determines whether accessing the accounts page returns a 404 code.'''
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 404)
