from unittest import TestCase
from app import create_app

class RouteTests(TestCase):
    def setUp(self):
        """Setup test client before each test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Cleanup after each test"""
        self.app_context.pop()

    def test_home_page(self):
        """
        Test whether the home page and form appears
        """
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>All Users</h1>', html)
        self.assertIn('action="/users/new"', html)