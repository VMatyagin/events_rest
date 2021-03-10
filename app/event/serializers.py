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

    brigades = BrigadeShortSerializer(many=True)

    participations = BoecShortSerializer(many=True)

    class Meta:
        model = EventOrder
        fields = ('id', 'brigades', 'participations', 'event',
                  'isСontender', 'place', 'title'
                  )
        read_only_fields = ('id', )
