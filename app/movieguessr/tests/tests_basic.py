''' Basic Tests '''

from django.test import TestCase


class BasicTestCase(TestCase):
    ''' Basic Case '''
    def setUp(self):
        ''' Set Up '''

    def test_home_access(self):
        ''' Test '''
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
