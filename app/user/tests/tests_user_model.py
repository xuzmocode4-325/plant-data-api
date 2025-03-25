from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from .. import models
from django.contrib.auth import get_user_model


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """
    Class for testing models.
    """

    def test_create_user_with_email_success(self):
        """Test for successful creation of user with email address."""
        username = 'testuser'
        email = 'test@example.com'
        password = 'test@123'
        user = get_user_model().objects.create_user(
            username, 
            email,
            password,
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_mormalized(self):
        """Test email mormalization for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
            ['Test5@Example.Com', 'Test5@example.com']
        ]
        for i, (email, expected) in enumerate(sample_emails):
            user = get_user_model().objects.create_user(f'test{i}', email, 'sample123')
            self.assertEqual(user.email, expected)

    @patch('user.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test generating image path"""

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.model_image_file_path(
            instance=None, 
            model='user',
            filename='profile.jpg'
        )
        self.assertEqual(file_path, f'uploads/user/{uuid}.jpg')

    def test_new_user_without_email_raises_error(self):
        """Test creating a new user without an email raises a value error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_staff_user(self):
        """Test createing a staff user."""
        user = get_user_model().objects.create_staff_user(
            'test@example.com',
            'test123'
        )
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_staff)
