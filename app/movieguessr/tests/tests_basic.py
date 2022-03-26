from django.test import TestCase


class BasicTestCase(TestCase):

    def setUp(self):
        pass

    def test_home_access(self):
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)