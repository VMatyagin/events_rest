from core.authentication import VKAuthentication
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManangeUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return authenticated user"""
        return self.request.user
