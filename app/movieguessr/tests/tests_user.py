'''Module for the User object tests.'''
from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User

class UserTests(TestCase):
    '''A class to represent the User object.'''

    def setUp(self):
        '''Setup method for user tests'''
        User.objects.create(username="Filippo", password='123456')

    def test_user_exists(self):
        '''Test to ensure that if searching for a user that does exist, the user gets returned.'''
        user = User.objects.get(username="Filippo") # User that does exist for sure.
        self.assertIsNotNone(user)

    def test_user_does_not_exists(self):
        '''Test to ensure that if searching for a user that does exist, null gets returned.'''
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="Filiiiiippo") # User that doesn't exist for sure.

    def test_username_is_unique(self):
        '''Test to check whether a provided username returns either 0 or 1 users and no more.'''
        users = User.objects.filter(username="Filippo")
        self.assertLessEqual(users.count(), 1)

    def test_user_with_username_exists(self):
        '''Test to check whether a new user with a duplicate username returns an error.'''
        with self.assertRaises(IntegrityError):
            User.objects.create(username="Filippo", password='123456')
