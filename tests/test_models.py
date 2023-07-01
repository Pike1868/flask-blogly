from unittest import TestCase
from app import create_app
from app.models import db, User


class ModelsTests(TestCase):
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

    def test_create_user(self):
        """Test creating a user"""
        new_user = User(first_name='John', last_name='Doe',
                        image_url='https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png')
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(first_name='John').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(
            user.image_url, 'https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png')

    def test_full_name(self):
        """Test full name method"""
        user = User.query.first()
        user_full_name = user.get_full_name
        self.assertEqual(user_full_name, f'{user.first_name} {user.last_name}')

    def test_delete_user(self):
        """Test deleting a user"""
        user = User.query.one_or_none()
        db.session.delete(user)
        db.session.commit()

        user = User.query.get(user.id)
        self.assertIsNone(user)
