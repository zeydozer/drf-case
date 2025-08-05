from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from users.models import Profile

User = get_user_model()


class UserPermissionsTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin_test",
            password="testpass",
            email="admin@test.com",
            role="admin"
        )
        
        self.staff_user = User.objects.create_user(
            username="staff_test",
            password="testpass",
            email="staff@test.com",
            role="staff"
        )
        
        self.viewer_user = User.objects.create_user(
            username="viewer_test",
            password="testpass",
            email="viewer@test.com",
            role="viewer"
        )

    def test_user_roles_assignment(self):
        """Test that users are assigned correct roles"""
        self.assertEqual(self.admin_user.role, "admin")
        self.assertEqual(self.staff_user.role, "staff")
        self.assertEqual(self.viewer_user.role, "viewer")

    def test_user_email_unique(self):
        """Test that email addresses must be unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="duplicate_email",
                password="testpass",
                email="admin@test.com",  # Same email as admin_user
                role="viewer"
            )

    def test_user_username_unique(self):
        """Test that usernames must be unique"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="admin_test",  # Same username as admin_user
                password="testpass",
                email="different@test.com",
                role="viewer"
            )

    def test_required_fields(self):
        """Test User model REQUIRED_FIELDS configuration"""
        self.assertEqual(User.REQUIRED_FIELDS, ['email'])
        self.assertEqual(User.USERNAME_FIELD, 'username')


class UserModelTest(TestCase):
    def test_user_creation_with_all_fields(self):
        """Test creating user with all fields"""
        user = User.objects.create_user(
            username="fulltest",
            password="testpass",
            email="full@test.com",
            first_name="Test",
            last_name="User",
            role="staff"
        )
        
        self.assertEqual(user.username, "fulltest")
        self.assertEqual(user.email, "full@test.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.role, "staff")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_meta_options(self):
        """Test User model meta options"""
        self.assertEqual(User._meta.verbose_name, 'User')
        self.assertEqual(User._meta.verbose_name_plural, 'Users')
