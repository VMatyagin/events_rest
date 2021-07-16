from core.authentication import VKAuthentication
from core.models import Activity, Boec
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings
from reversion.views import RevisionMixin
from so import serializers
from user.serializers import ActivitySerailizer, AuthTokenSerializer, UserSerializer


class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManangeUserView(generics.RetrieveAPIView):
    """manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return authenticated user"""
        return self.request.user


class ActivityView(RevisionMixin, viewsets.ViewSet):
    """manage the activities"""

    serializer_class = ActivitySerailizer
    authentication_classes = (VKAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def retrieve(self, request, pk=None):
        try:
            boec = Boec.objects.get(vkId=self.request.user.vkId)
            activities = Activity.objects.filter(boec=boec, seen=False)
            serializer = ActivitySerailizer(activities, many=True)
        except (Boec.DoesNotExist, ValidationError):
            msg = _("Boec doesnt exists.")
            raise ValidationError({"error": msg}, code="validation")
        return Response(serializer.data)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated),
        url_path="markAsRead",
        url_name="markAsRead",
        authentication_classes=(VKAuthentication,),
    )
    def markAsRead(self, request, pk=None):
        try:
            boec = Boec.objects.get(vkId=self.request.user.vkId)
            Activity.objects.filter(boec=boec, seen=False).update(seen=True)

        except (Boec.DoesNotExist, ValidationError):
            msg = _("Boec doesnt exists.")
            raise ValidationError({"error": msg}, code="validation")

        return Response({})
