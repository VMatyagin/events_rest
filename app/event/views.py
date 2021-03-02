from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication

from reversion.views import RevisionMixin

from core.models import Event
from event import serializers


class EventViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage events in the database"""
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')
