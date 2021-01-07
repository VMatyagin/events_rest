from rest_framework import serializers

from core.models import Area, Boec, Shtab


class ShtabSerializer(serializers.ModelSerializer):
    """serializer for the shtab objects"""

    class Meta:
        model = Shtab
        fields = ('id', 'title')
        read_only_fields = ('id',)


class AreaSerializer(serializers.ModelSerializer):
    """serializer for area objects"""

    class Meta:
        model = Area
        fields = ('id', 'title', 'shortTitle')
        read_only_fields = ('id',)


class BoecSerializer(serializers.ModelSerializer):
    """serializer for beec objects"""

    class Meta:
        model = Boec
        fields = ('id', 'firstName', 'lastName', 'middleName', 'DOB')
        read_only_fields = ('id',)
