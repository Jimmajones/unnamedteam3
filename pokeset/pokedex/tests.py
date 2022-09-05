from django.test import TestCase

class AccessViewTestCase(TestCase):
    """
    Set of test cases that test access to the webpages of the website
    """

    def test_login_access(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_access(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_without_login_path_access(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)