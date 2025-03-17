from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users (is_staff=True) to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is staff using the token payload
        return request.user.is_staff