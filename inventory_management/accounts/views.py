from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering new users.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
