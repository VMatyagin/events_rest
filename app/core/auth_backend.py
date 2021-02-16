from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(request=None, vk_id=None):
        try:
            return get_user_model().objects.get(vk_id=vk_id)
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, vk_id):
        try:
            return get_user_model().objects.get(vk_id=vk_id)
        except get_user_model().DoesNotExist:
            return None
