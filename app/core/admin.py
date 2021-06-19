import logging

from core import models
from core.auth_backend import PasswordlessAuthBackend
from django import forms
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext as _
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from reversion_compare.admin import CompareVersionAdmin

authenticate = PasswordlessAuthBackend.authenticate
logger = logging.getLogger(__name__)


class LoginForm(AdminAuthenticationForm):
    """
    Class for authenticating users by vk id
    """

    username = UsernameField(
        label=_("VK id"), widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = None

    error_messages = {
        "invalid_login": _("Please enter a correct %(username)s."),
        "inactive": _("This account is inactive."),
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
            get_user_model().USERNAME_FIELD
        )

    def clean(self):
        username = self.cleaned_data.get("username")

        if username is not None:
            self.user_cache = authenticate(self.request, vkId=username)
            logger.error(self.user_cache is None)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserAdmin(CompareVersionAdmin, BaseUserAdmin):
    ordering = ["id"]
    list_display = ["vkId", "name"]
    fieldsets = (
        (None, {"fields": ("vkId",)}),
        (_("Personal Info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("vkId",)}),)


class SeasonAdmin(CompareVersionAdmin, admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["boec", "brigade", "year"]
    search_fields = ("boec__lastName", "boec__firstName")
    list_filter = ("brigade", "year")


class ShtabAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class AreaAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class BoecAdmin(CompareVersionAdmin, admin.ModelAdmin):
    ordering = ["lastName"]
    search_fields = ("lastName", "firstName")


class BrigadeAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class EventAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class ActivePositionFilter(admin.SimpleListFilter):
    title = _("Действующий")
    parameter_name = "toDate"

    def lookups(self, request, model_admin):
        return (("0", _("Действующий")), ("1", _("Не действующий")))

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(toDate__isnull=True)
        if self.value() == "1":
            return queryset.filter(toDate__isnull=False)


class PositionAdmin(CompareVersionAdmin, admin.ModelAdmin):
    list_display = ["position", "brigade", "boec"]
    list_filter = ("position", ActivePositionFilter, ("brigade", RelatedDropdownFilter))


class ParticipantAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class CompetitionAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class CompetitionParticipantAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class NominationAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


class ConferenceAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Shtab, ShtabAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Boec, BoecAdmin)
admin.site.register(models.Brigade, BrigadeAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.Position, PositionAdmin)
admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.Competition, CompetitionAdmin)
admin.site.register(models.CompetitionParticipant, CompetitionParticipantAdmin)
admin.site.register(models.Nomination, NominationAdmin)
admin.site.register(models.Conference, ConferenceAdmin)
