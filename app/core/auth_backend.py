from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(self, request=None, vkId=None):
        try:
            return get_user_model().objects.get(vkId=vkId)
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, vkId):
        try:
            return get_user_model().objects.get(vkId=vkId)
        except get_user_model().DoesNotExist:
            return None
