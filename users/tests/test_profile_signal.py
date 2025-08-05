from rest_framework.test import APITestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


class ProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        """Test that profile is automatically created when user is created"""
        user = User.objects.create_user(
            username="withprofile", 
            password="testpass",
            email="profile@test.com",
            role="staff"
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())
        
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertFalse(profile.is_verified)  # Default value
        self.assertEqual(profile.bio, "")  # Default empty bio

    def test_profile_not_created_twice(self):
        """Test that profile is not duplicated on user update"""
        user = User.objects.create_user(
            username="updatetest",
            password="testpass",
            email="update@test.com",
            role="viewer"
        )
        
        # Check initial profile creation
        initial_profile_count = Profile.objects.filter(user=user).count()
        self.assertEqual(initial_profile_count, 1)
        
        # Update user
        user.first_name = "Updated"
        user.save()
        
        # Check that no additional profile was created
        final_profile_count = Profile.objects.filter(user=user).count()
        self.assertEqual(final_profile_count, 1)

    def test_profile_str_method(self):
        """Test Profile model string representation"""
        user = User.objects.create_user(
            username="strprofiletest",
            password="testpass",
            email="strprofile@test.com",
            role="admin"
        )
        profile = Profile.objects.get(user=user)
        expected_str = f"Profile of {user.username}"
        self.assertEqual(str(profile), expected_str)

    def test_profile_verification_status(self):
        """Test profile verification status can be updated"""
        user = User.objects.create_user(
            username="verifytest",
            password="testpass",
            email="verify@test.com",
            role="staff"
        )
        
        profile = Profile.objects.get(user=user)
        self.assertFalse(profile.is_verified)
        
        # Update verification status
        profile.is_verified = True
        profile.save()
        
        # Reload from database
        profile.refresh_from_db()
        self.assertTrue(profile.is_verified)

    def test_profile_bio_update(self):
        """Test profile bio can be updated"""
        user = User.objects.create_user(
            username="biotest",
            password="testpass",
            email="bio@test.com",
            role="viewer"
        )
        
        profile = Profile.objects.get(user=user)
        test_bio = "This is a test bio for the user."
        profile.bio = test_bio
        profile.save()
        
        # Reload from database
        profile.refresh_from_db()
        self.assertEqual(profile.bio, test_bio)
