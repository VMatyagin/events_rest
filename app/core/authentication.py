
from base64 import b64encode
from hashlib import sha256
from hmac import HMAC
from urllib.parse import parse_qsl, urlencode, urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

# Защищённый ключ из настроек вашего приложения
client_secret = "wvl68m4dR1UpLrVRli"


def is_valid(query: dict, secret: str) -> bool:
    """

    Check VK Apps signature

    :param dict query: Словарь с параметрами запуска
    :param str secret: Секретный ключ приложения ("Защищённый ключ")
    :returns: Результат проверки подписи
    :rtype: bool

    """
    if not query.get("sign"):
        return False

    vk_subset = sorted(
        filter(
            lambda key: key.startswith("vk_"),
            query
        )
    )

    if not vk_subset:
        return False

    ordered = {k: query[k] for k in vk_subset}

    hash_code = b64encode(
        HMAC(
            secret.encode(),
            urlencode(ordered, doseq=True).encode(),
            sha256
        ).digest()
    ).decode("utf-8")

    if hash_code[-1] == "=":
        hash_code = hash_code[:-1]

    fixed_hash = hash_code.replace('+', '-').replace('/', '_')
    return query.get("sign") == fixed_hash


class VKAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'VK'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        # if not auth or auth[0].lower() != self.keyword.lower().encode():
        #     return None

        if len(auth) != 1:
            msg = _('Invalid token header')
            raise exceptions.AuthenticationFailed(msg)

        try:
            query_params = dict(
                parse_qsl(
                    urlparse(auth[0].decode()).path,
                    keep_blank_values=True
                )
            )
        except UnicodeError:
            msg = _(
                'Invalid token header. '
                'Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(query_params)

    def authenticate_credentials(self, query_params):
        if settings.DEBUG:
            is_sign_validated = True
        else:
            is_sign_validated = is_valid(
                query=query_params, secret=client_secret)
        if (not is_sign_validated):
            raise exceptions.AuthenticationFailed(
                _('Sign is not valid.'))
        try:
            user = get_user_model().objects.get(
                vk_id=query_params.get('vk_user_id')
            )
            if not user.is_active:
                raise exceptions.AuthenticationFailed(
                    _('User inactive or deleted.'))
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                _("Invalid token or user doesn't exist."))

        return (user, query_params.get('vk_user_id'))

    def authenticate_header(self, request):
        return self.keyword
