from rest_framework.permissions import BasePermission

class IsRole(BasePermission):
  def __init__(self, allowed_roles):
    self.allowed_roles = allowed_roles

  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    return hasattr(request.user, 'profile') and request.user.profile.role in self.allowed_roles
