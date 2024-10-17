from rest_framework import permissions
from base.models import Student

class IsLibrarian(permissions.BasePermission):
  def has_permission(self, request, view):
    return request.user.groups.filter(name='Librarian').exists()
  
class IsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.student == request.user
    return super().has_object_permission(request, view, obj)