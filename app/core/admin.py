from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UsernameField
from core import models
from core.auth_backend import PasswordlessAuthBackend
from django.utils.text import capfirst

from reversion_compare.admin import CompareVersionAdmin

import logging
logger = logging.getLogger(__name__)
authenticate = PasswordlessAuthBackend.authenticate


class LoginForm(AdminAuthenticationForm):
    """
    Class for authenticating users by vk id
    """
    username = UsernameField(
        label=_("VK id"), widget=forms.TextInput(attrs={'autofocus': True}))
    password = None

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = get_user_model()._meta.get_field(
            get_user_model().USERNAME_FIELD)
        self.fields['username'].max_length = (
            self.username_field.max_length or 25
        )
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')

        if username is not None:
            self.user_cache = authenticate(
                self.request, vk_id=username)
            if self.user_cache is None:

                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserAdmin(CompareVersionAdmin, BaseUserAdmin):
    ordering = ['id']
    list_display = ['vk_id', 'name']
    fieldsets = (
        (None, {'fields': ('vk_id',)}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('vk_id',)
        }),
    )


class SeasonAdmin(CompareVersionAdmin, admin.ModelAdmin):
    ordering = ['id']
    list_display = ['boec', 'brigade', 'year']
    search_fields = ('boec__lastName', 'boec__firstName')
    list_filter = ('brigade', 'year')


class ShtabAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class AreaAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class BoecAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class BrigadeAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class EventAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Shtab, ShtabAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Boec, BoecAdmin)
admin.site.register(models.Brigade, BrigadeAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Season, SeasonAdmin)
