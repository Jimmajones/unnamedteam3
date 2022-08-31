from django.test import TestCase

class AccessViewTestCase(TestCase):
    """
    Set of test cases that test access to the webpages of the website
    """

    def test_dashboard_access(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_detailed_view_access(self):
        response = self.client.get('/detailed_view/0/')
        self.assertEqual(response.status_code, 200)

    def test_edit_pokemon_access(self):
        response = self.client.get('/edit_pokemon/0')
        self.assertEqual(response.status_code, 200)