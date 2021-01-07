from rest_framework import serializers

from core.models import Event


class EventSerializer(serializers.ModelSerializer):
    """serializer for the event objects"""

    class Meta:
        model = Event
        fields = ('id', 'status', 'title', 'description',
                  'location', 'shtab', 'start', 'end', 'organizer',
                  'volonteer', 'visibility')
        read_only_fields = ('id',)
