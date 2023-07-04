from unittest import TestCase
from app import create_app
from app.models import db, User


class RouteTests(TestCase):
    def setUp(self):
        """Setup test client before each test"""
        self.app = create_app('Testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Clear data and create new tables
        db.drop_all()
        db.create_all()

        # Add test user
        users_data = [
            {'first_name': 'John', 'last_name': 'Doe'},
        ]

        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit()

    def tearDown(self):
        """Cleanup after each test"""
        db.session.remove()
        self.app_context.pop()

    def test_home_page(self):
        """
        Test whether the home page and list of recent posts appears
        """
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Blogly Recent Posts</h1>', html)
        self.assertIn('ul', html)
        self.assertIn('action="/users"', html)
        self.assertIn('method="get',html)

    def test_users_page(self):
        """
        Test whether the list of users appears on /users route
        """
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>All Users</h1>', html)
        self.assertIn('action="/users/new"', html)

    def test_users_form(self):
        """
        Test whether the home page and form appears
        """
        resp = self.client.get('/users/new')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('action="/users/new"', html)
        self.assertIn('method="POST"', html)
        self.assertIn('id="first_name_input"', html)
        self.assertIn('id="last_name_input"', html)
        self.assertIn('id="image_url_input"', html)

    def test_show_user(self):
        """Test showing a specific user"""
        user = User.query.first()
        resp = self.client.get(f'/users/{user.id}')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(f'<h1>{user.first_name} {user.last_name}</h1>', html)

    def test_add_user(self):
        """Test adding a user"""
        data = {'first_name': 'New', 'last_name': 'User', 'image_url': ''}
        resp = self.client.post('/users/new', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>All Users</h1>', html)
        self.assertIn('<li><a href="/users/1">John Doe</a></li>', html)
        self.assertIn('<li><a href="/users/2">New User</a></li>', html)

    def test_edit_user(self):
        """Test editing a user"""
        user = User.query.first()
        data = {'first_name': 'Edited', 'last_name': 'User', 'image_url': ''}
        resp = self.client.post(
            f'/users/{user.id}/edit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>All Users</h1>', html)
        self.assertIn('<li><a href="/users/1">Edited User</a></li>', html)

    def test_delete_user(self):
        """Test deleting a user"""
        user = User.query.first()
        resp = self.client.post(
            f'/users/{user.id}/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(f'<h1>{user.first_name} {user.last_name}</h1>', html)
