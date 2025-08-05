from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


class AuthTest(APITestCase):
    def test_user_registration(self):
        """Test user registration with role assignment"""
        url = reverse('register')
        data = {
            "username": "zeydtest",
            "email": "zeyd@test.com",
            "password": "supersecure",
            "role": "viewer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        
        user = User.objects.get(username="zeydtest")
        self.assertTrue(User.objects.filter(username="zeydtest").exists())
        self.assertEqual(user.role, "viewer")
        self.assertEqual(user.email, "zeyd@test.com")

    def test_user_registration_with_different_roles(self):
        """Test user registration with different roles"""
        roles = ['viewer', 'staff', 'admin']
        
        for i, role in enumerate(roles):
            url = reverse('register')
            data = {
                "username": f"testuser_{i}",
                "email": f"test{i}@example.com",
                "password": "testpass123",
                "role": role
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, 201)
            
            user = User.objects.get(username=f"testuser_{i}")
            self.assertEqual(user.role, role)

    def test_token_obtain_success(self):
        """Test successful token generation"""
        User.objects.create_user(
            username="zeydlogin", 
            password="secret123",
            email="login@test.com",
            role="staff"
        )
        url = reverse('token_obtain_pair')
        data = {"username": "zeydlogin", "password": "secret123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtain_fail(self):
        """Test token generation with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {"username": "fakeuser", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn("No active account", str(response.data))

    def test_token_refresh(self):
        """Test token refresh functionality"""
        user = User.objects.create_user(
            username="refreshtest", 
            password="secret123",
            email="refresh@test.com",
            role="viewer"
        )
        
        # Get initial tokens
        url = reverse('token_obtain_pair')
        data = {"username": "refreshtest", "password": "secret123"}
        response = self.client.post(url, data, format='json')
        refresh_token = response.data["refresh"]
        
        # Test refresh
        refresh_url = reverse('token_refresh')
        refresh_data = {"refresh": refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.data)

    def test_user_profile_creation(self):
        """Test that profile is automatically created for new users"""
        user = User.objects.create_user(
            username="profiletest",
            password="testpass",
            email="profile@test.com",
            role="staff"
        )
        
        # Check if profile was created
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertFalse(profile.is_verified)  # Default value

    def test_user_str_method(self):
        """Test User model string representation"""
        user = User.objects.create_user(
            username="strtest",
            password="testpass",
            email="str@test.com",
            role="admin"
        )
        self.assertEqual(str(user), "strtest")

    def test_user_role_default(self):
        """Test default role assignment"""
        user = User.objects.create_user(
            username="defaultrole",
            password="testpass",
            email="default@test.com"
        )
        self.assertEqual(user.role, "viewer")  # Default role
