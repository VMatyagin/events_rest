from rest_framework import serializers

from core.models import Brigade, Event, EventOrder
from so.serializers import BoecShortSerializer, BrigadeShortSerializer


class EventSerializer(serializers.ModelSerializer):
    """serializer for the event objects"""

    class Meta:
        model = Event
        fields = ('id', 'status', 'title', 'description',
                  'location', 'shtab', 'startDate', 'startTime',
                  'visibility', 'worth')
        read_only_fields = ('id', )


class OrderSerializer(serializers.ModelSerializer):
    """serializer for the eventorders objects"""

    brigade = BrigadeShortSerializer(read_only=True)
    brigade_id = serializers.PrimaryKeyRelatedField(
        queryset=Brigade.objects.all(),
        source='brigade')

    participations = BoecShortSerializer(many=True, read_only=True)

    class Meta:
        model = EventOrder
        fields = ('id', 'brigade', 'participations', 'event',
                  'isСontender', 'place', 'brigade_id', 'title'
                  )
        read_only_fields = ('id', 'brigade')
