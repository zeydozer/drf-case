from rest_framework import serializers
from .models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  role = serializers.CharField(required=False)

  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']

  def create(self, validated_data):
    role = validated_data.pop('role', 'viewer')  # Default to viewer if not provided
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
      role=role,
      first_name=validated_data.get('first_name', ''),
      last_name=validated_data.get('last_name', '')
    )
    return user


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['bio', 'is_verified', 'created_at']
    read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer(read_only=True)
  
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined', 'profile']
    read_only_fields = ['id', 'date_joined']
