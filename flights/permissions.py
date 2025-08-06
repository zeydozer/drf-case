from rest_framework.permissions import BasePermission

class IsStaffOrAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user and request.user.role in ['staff', 'admin']