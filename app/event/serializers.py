import logging

from core.models import (
    Boec,
    Brigade,
    Competition,
    CompetitionParticipant,
    Event,
    Nomination,
    Participant,
    Season,
    Shtab,
    Ticket,
)
from core.serializers import DynamicFieldsModelSerializer
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from so.serializers import BoecInfoSerializer, BrigadeShortSerializer, ShtabSerializer

logger = logging.getLogger(__name__)


class EventSerializer(DynamicFieldsModelSerializer):
    """serializer for the event objects"""

    shtab = ShtabSerializer(read_only=True)
    shtabId = serializers.PrimaryKeyRelatedField(
        queryset=Shtab.objects.all(), source="shtab", required=False
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "status",
            "title",
            "description",
            "location",
            "shtab",
            "startDate",
            "startTime",
            "visibility",
            "worth",
            "shtabId",
            "isTicketed",
        )
        read_only_fields = ("id", "shtab")


class ParticipantSerializer(DynamicFieldsModelSerializer):
    """serializer for participants"""

    event = EventSerializer(fields=("id", "title"), required=False)
    eventId = serializers.PrimaryKeyRelatedField(
        queryset=Brigade.objects.all(), source="event", required=False
    )

    boec = BoecInfoSerializer(required=False)
    boecId = serializers.PrimaryKeyRelatedField(
        queryset=Boec.objects.all(), source="boec"
    )

    def validate_boecId(self, value):
        participant = Participant.objects.filter(
            event=self.context["event_pk"], boec=value
        )
        if participant:
            raise serializers.ValidationError(
                {"error": "Boec already included"}, code="validation"
            )
        return value

    def validate(self, attrs):
        try:
            Event.objects.get(id=self.context["event_pk"])
        except (Event.DoesNotExist):
            msg = _("Invalid event")
            raise serializers.ValidationError({"error": msg}, code="validation")

        return super().validate(attrs)

    class Meta:
        model = Participant
        fields = ("id", "boec", "event", "worth", "boecId", "eventId", "brigade")
        read_only_fields = ("id", "boec", "event")


class CompetitionSerializer(DynamicFieldsModelSerializer):
    """serializer for Competition"""

    def validate(self, attrs):
        if "event_pk" in self.context:
            try:
                Event.objects.get(id=self.context["event_pk"])
            except (Event.DoesNotExist):
                msg = _("Invalid event")
                raise serializers.ValidationError({"error": msg}, code="validation")
        return super().validate(attrs)

    participant_count = serializers.SerializerMethodField("get_participant_count")

    def get_participant_count(self, obj):
        return obj.competition_participation.filter(worth=0).count()

    ivolvement_count = serializers.SerializerMethodField("get_ivolvement_count")

    def get_ivolvement_count(self, obj):
        return obj.competition_participation.filter(worth=1).count()

    winner_count = serializers.SerializerMethodField("get_winner_count")

    def get_winner_count(self, obj):
        return obj.competition_participation.filter(
            worth=1, nomination__isnull=False, nomination__isRated=True
        ).count()

    notwinner_count = serializers.SerializerMethodField("get_notwinner_count")

    def get_notwinner_count(self, obj):
        return obj.competition_participation.filter(
            worth=1, nomination__isnull=False, nomination__isRated=False
        ).count()

    class Meta:
        model = Competition
        fields = (
            "id",
            "event",
            "title",
            "participant_count",
            "ivolvement_count",
            "winner_count",
            "notwinner_count",
            "ratingless",
        )
        read_only_fields = (
            "id",
            "participant_count",
            "ivolvement_count",
            "winner_count",
            "notwinner_count",
        )
        extra_kwargs = {"event": {"required": False}}


class NominationSerializer(DynamicFieldsModelSerializer):
    """serializer for Competition"""

    def validate(self, attrs):
        if "competition_pk" in self.context:
            try:
                Competition.objects.get(id=self.context["competition_pk"])
            except (Competition.DoesNotExist):
                msg = _("Invalid Competition")
                raise serializers.ValidationError({"error": msg}, code="validation")
        return super().validate(attrs)

    class Meta:
        model = Nomination
        fields = ("id", "competition", "title", "isRated", "sportPlace")
        read_only_fields = ("id",)
        extra_kwargs = {"competition": {"required": False}}


class CompetitionParticipantsSerializer(DynamicFieldsModelSerializer):
    """serializer for participants Competition"""

    def validate(self, attrs):
        if "competition_pk" in self.context:
            try:
                Competition.objects.get(id=self.context["competition_pk"])
            except (Competition.DoesNotExist):
                msg = _("Invalid Competition")
                raise serializers.ValidationError({"error": msg}, code="validation")
        return super().validate(attrs)

    def create(self, validated_data):
        brigades_list = list()
        boec_list = list()
        if "brigades" in validated_data:
            brigades_list = validated_data.pop("brigades")
        if "boec" in validated_data:
            boec_list = validated_data.pop("boec")

        instance = CompetitionParticipant.objects.create(**validated_data)

        if len(brigades_list) > 0:
            instance.brigades.set(brigades_list)

        if len(boec_list) > 0:
            instance.boec.set(boec_list)
            if len(brigades_list) == 0:
                brigade_list = set()
                for boec in boec_list:
                    boec_last_season = (
                        # getting the last boec's Season
                        Season.objects.filter(boec=boec)
                        .order_by("year")
                        .last()
                    )

                    brigade_list.add(boec_last_season.brigade)
                instance.brigades.set(brigade_list)

        return instance

    def update(self, instance, validated_data):
        if "worth" in validated_data and validated_data["worth"] == 1:
            if "nominationId" in self.context["request"].data:
                nomination = Nomination.objects.get(
                    id=self.context["request"].data["nominationId"]
                )

                nomination.owner.add(instance)

        if (
            "worth" in validated_data
            and validated_data["worth"] < 1
            and instance.nomination.count() > 0
        ):
            for nomination in instance.nomination.iterator():
                nomination.owner.remove(instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super(
            CompetitionParticipantsSerializer, self
        ).to_representation(instance)
        # восстановить, если понадобятся ФИО
        # representation['boec'] = BoecInfoSerializer(
        #     instance.boec.all(), many=True).data
        return representation

    brigadesIds = serializers.PrimaryKeyRelatedField(
        queryset=Brigade.objects.all(), source="brigades", many=True, required=False
    )

    brigades = BrigadeShortSerializer(many=True, read_only=True)
    nomination = NominationSerializer(many=True, read_only=True, fields=("id", "title"))

    class Meta:
        model = CompetitionParticipant
        fields = (
            "id",
            "competition",
            "boec",
            "worth",
            "brigades",
            "nomination",
            "brigades",
            "brigadesIds",
            "title",
        )
        read_only_fields = ("id", "brigades")
        extra_kwargs = {
            "competition": {"required": False},
            "nomination": {"required": False},
        }


class TicketSerializer(DynamicFieldsModelSerializer):
    """Serializer for tickets"""

    event = EventSerializer(read_only=True)
    boec = BoecInfoSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "uuid",
            "boec",
            "event",
            "createdAt",
            "updatedAt",
        )
        read_only_fields = ("id",)
