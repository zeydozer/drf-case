from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class AuthTest(APITestCase):
  def test_user_registration(self):
    url = reverse('register')
    data = {
      "username": "zeydtest",
      "email": "zeyd@test.com",
      "password": "supersecure"
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertTrue(User.objects.filter(username="zeydtest").exists())

  def test_token_obtain_success(self):
    User.objects.create_user(username="zeydlogin", password="secret123")
    url = reverse('token_obtain_pair')
    data = {"username": "zeydlogin", "password": "secret123"}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)

  def test_token_obtain_fail(self):
    url = reverse('token_obtain_pair')
    data = {"username": "fakeuser", "password": "wrongpass"}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 401)
    self.assertIn("No active account", str(response.data))
