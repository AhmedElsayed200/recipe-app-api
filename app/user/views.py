# views.py
from rest_framework import generics, authentication, permissions

from .serializers import (
    UserSerializer,
    TokenSerializer
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

class TokenCreateView(ObtainAuthToken):
    """ create new auth token for users """
    serializer_class = TokenSerializer
    # renderer_classes = api_settings.DEFAULT.RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user