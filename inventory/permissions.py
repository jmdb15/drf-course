from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
  def has_permission(self, request, view):
    return True