from rest_framework.test import APITestCase
from users.models import User
from users.models import Profile

class ProfileSignalTest(APITestCase):
  def test_profile_created_on_user_creation(self):
    user = User.objects.create_user(username="withprofile", password="testpass")
    self.assertTrue(Profile.objects.filter(user=user).exists())
