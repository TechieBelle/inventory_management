from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from .serializers import UserSerializer

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only admins full CRUD. 
    Regular users can only view their own profile.
    """

    def has_permission(self, request, view):
        # Allow read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow admins for write requests
        return request.user and request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
