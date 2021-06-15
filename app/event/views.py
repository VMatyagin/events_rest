from django.core.exceptions import ValidationError
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication
from rest_framework import filters

from reversion.views import RevisionMixin

from core import models
from core.utils.sheets import EventReportGenerator
from event import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response


class CreateListAndDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    pass


class EventViewSet(RevisionMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """manage events in the database"""
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    filter_backends = [filters.SearchFilter]
    search_fields = ('title', )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-startDate')

    @action(methods=['post'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='report', url_name='report',
            authentication_classes=(VKAuthentication,)
            )
    def generateReport(self, request, pk):
        event = models.Event.objects.get(id=pk)
        reporter = EventReportGenerator(
            '1s_NVTmYxG5GloDaOOw4d7eh7P_zAcobTmIRseYHsg3g')
        url = reporter.create(event)

        return Response(url)


class EventParticipant(RevisionMixin, CreateListAndDestroyViewSet):
    """manage participants in the database"""
    serializer_class = serializers.ParticipantSerializer
    queryset = models.Participant.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return models.Participant.objects.filter(event=self.kwargs['_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['_pk'] = self.kwargs['_pk']
        return context

    def perform_create(self, serializer, worth):
        eventId = self.kwargs['_pk']
        event = models.Event.objects.get(id=eventId)

        serializer.save(event=event, worth=worth)


class EventReport(RevisionMixin, mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    pass


class EventOrganizers(EventParticipant):
    def get_queryset(self):
        return super().get_queryset().filter(worth=1)

    def perform_create(self, serializer):
        return super().perform_create(serializer, 1)


class EventVolonteers(EventParticipant):
    def get_queryset(self):
        return super().get_queryset().filter(worth=0)

    def perform_create(self, serializer):
        return super().perform_create(serializer, 0)
