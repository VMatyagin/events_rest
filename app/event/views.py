import logging
from threading import Thread

from core import models
from core.authentication import VKAuthentication
from core.utils.sheets import EventReportGenerator
from django.core.exceptions import ValidationError
from event import serializers
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reversion.views import RevisionMixin

logger = logging.getLogger(__name__)


class CreateListAndDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class EventViewSet(
    RevisionMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """manage events in the database"""

    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = [filters.SearchFilter]
    search_fields = ("title",)

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by("-startDate")

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="report",
        url_name="report",
        authentication_classes=(VKAuthentication,),
    )
    def generateReport(self, request, pk):
        event = models.Event.objects.get(id=pk)
        reporter = EventReportGenerator("1s_NVTmYxG5GloDaOOw4d7eh7P_zAcobTmIRseYHsg3g")
        Thread(target=reporter.create, args=[event]).start()

        return Response({})


class EventParticipant(RevisionMixin, CreateListAndDestroyViewSet):
    """manage participants in the database"""

    serializer_class = serializers.ParticipantSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        worth = self.request.query_params.get("worth", None)
        if worth is not None:
            return models.Participant.objects.filter(
                event=self.kwargs["event_pk"], worth=worth
            )
        return models.Participant.objects.filter(event=self.kwargs["event_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["event_pk"] = self.kwargs["event_pk"]
        return context

    def perform_create(self, serializer):
        eventId = self.kwargs["event_pk"]
        event = models.Event.objects.get(id=eventId)

        serializer.save(event=event)


class EventCompetitionListCreate(
    RevisionMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """manage event competitions in the database"""

    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if "event_pk" in self.kwargs:
            return models.Competition.objects.filter(event=self.kwargs["event_pk"])
        return models.Competition.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "event_pk" in self.kwargs:
            context["event_pk"] = self.kwargs["event_pk"]
        return context

    def perform_create(self, serializer):
        if "event_pk" in self.kwargs:
            eventId = self.kwargs["event_pk"]
            event = models.Event.objects.get(id=eventId)
            serializer.save(event=event)
        else:
            super().perform_create(serializer)


class EventCompetitionRetrieveUpdateDestroy(
    RevisionMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """manage event competitions in the database"""

    serializer_class = serializers.CompetitionSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = models.Competition.objects.all()


class EventCompetitionParticipants(RevisionMixin, viewsets.ModelViewSet):
    """manage event competitions in the database"""

    serializer_class = serializers.CompetitionParticipantsSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.CompetitionParticipant.objects.all()
        worth = self.request.query_params.get("worth", None)
        if "competition_pk" in self.kwargs:
            queryset = queryset.filter(competition=self.kwargs["competition_pk"])
        if worth is not None:
            queryset = queryset.filter(worth=worth)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "competition_pk" in self.kwargs:
            context["competition_pk"] = self.kwargs["competition_pk"]
        return context

    def perform_create(self, serializer):
        if "competition_pk" not in self.kwargs:
            raise ValidationError(
                {
                    "error": "You should not use this endpoint for creating "
                    "CompetitionParticipant objects "
                },
                code="validation",
            )
        competitionId = self.kwargs["competition_pk"]
        competition = models.Competition.objects.get(id=competitionId)
        serializer.save(competition=competition)


class NominationView(RevisionMixin, viewsets.ModelViewSet):
    """manage event competitions in the database"""

    serializer_class = serializers.NominationSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Nomination.objects.all()
        if "competition_pk" in self.kwargs:
            queryset = queryset.filter(competition=self.kwargs["competition_pk"])
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "competition_pk" in self.kwargs:
            context["competition_pk"] = self.kwargs["competition_pk"]
        return context

    def perform_create(self, serializer):
        if "competition_pk" not in self.kwargs:
            raise ValidationError(
                {
                    "error": "You should not use this endpoint for creating "
                    "CompetitionParticipant objects "
                },
                code="validation",
            )
        competitionId = self.kwargs["competition_pk"]
        competition = models.Competition.objects.get(id=competitionId)
        serializer.save(competition=competition)

    def perform_destroy(self, instance):
        owner = instance.owner.all()
        if owner.count() > 0:
            for owner in owner.iterator():
                logger.error(owner)
                owner.worth = 1
                owner.save()

        return super().perform_destroy(instance)
