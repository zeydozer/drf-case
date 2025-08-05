
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  email = models.EmailField(unique=True)
  role = models.CharField(max_length=20, default='viewer')  # viewer, staff, admin

  REQUIRED_FIELDS = ['email']
  USERNAME_FIELD = 'username'

  def __str__(self):
    return self.username

  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True)
  is_verified = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Profile of {self.user.username}"
