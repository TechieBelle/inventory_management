from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only admins full CRUD.
    Regular users can only view their own profile (read-only).
    """

    def has_permission(self, request, view):
        # Allow read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can create/update/delete users
        return request.user and request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    """
    Admins can manage all users.
    Normal users can only view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class RegisterView(generics.CreateAPIView):
    """
    Public endpoint to register new users.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
