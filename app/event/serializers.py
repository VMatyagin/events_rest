from rest_framework import serializers

from core.models import Boec, Brigade, Event, Participant, Shtab
from core.serializers import DynamicFieldsModelSerializer
from so.serializers import BoecInfoSerializer, ShtabSerializer
from django.utils.translation import ugettext_lazy as _


class EventSerializer(DynamicFieldsModelSerializer):
    """serializer for the event objects"""

    shtab = ShtabSerializer(read_only=True)
    shtabId = serializers.PrimaryKeyRelatedField(
        queryset=Shtab.objects.all(),
        source='shtab'
    )

    class Meta:
        model = Event
        fields = ('id', 'status', 'title', 'description',
                  'location', 'shtab', 'startDate', 'startTime',
                  'visibility', 'worth', 'shtabId')
        read_only_fields = ('id', 'shtab')


class ParticipantSerializer(DynamicFieldsModelSerializer):
    """serializer for participants"""

    event = EventSerializer(fields=('id', 'title'), required=False)
    eventId = serializers.PrimaryKeyRelatedField(
        queryset=Brigade.objects.all(),
        source='event',
        required=False

    )

    boec = BoecInfoSerializer(required=False)
    boecId = serializers.PrimaryKeyRelatedField(
        queryset=Boec.objects.all(),
        source='boec',
    )

    worth = serializers.IntegerField(required=False)

    def validate_boecId(self, value):
        participant = Participant.objects.filter(
            event=self.context['_pk'],
            boec=value
        )
        if participant:
            raise serializers.ValidationError(
                {'error': 'Boec already included'}, code='validation'
            )
        return value

    def validate(self, attrs):
        try:
            Event.objects.get(id=self.context['_pk'])
        except (Event.DoesNotExist):
            msg = _('Invalid event')
            raise serializers.ValidationError(
                {'error': msg}, code='validation')

        return super().validate(attrs)

    class Meta:
        model = Participant
        fields = ('id', 'boec', 'event', 'worth', 'boecId', 'eventId')
        read_only_fields = ('id', 'boec', 'event')
