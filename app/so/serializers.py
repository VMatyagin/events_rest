from django.db import models
from rest_framework import serializers

from core.models import Area, Boec, Brigade, Season, Shtab


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


class BrigadeShortSerializer(serializers.ModelSerializer):
    """serializer with only id and title"""

    class Meta:
        model = Brigade
        fields = ('id', 'title')
        read_only_fields = ('id', )


class SeasonSerializer(serializers.ModelSerializer):
    """serializer for season objects"""

    brigade = BrigadeShortSerializer(read_only=True)
    brigade_id = serializers.PrimaryKeyRelatedField(queryset=Brigade.objects.all(), source='brigade')

    class Meta:
        model = Season
        fields = ('id', 'boec', 'brigade', 'year', 'brigade_id')
        read_only_fields = ('id', )


class BoecShortSerializer(serializers.ModelSerializer):
    """serializer for boec objects"""
    fullName = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        return f"{obj.lastName} {obj.firstName} {obj.middleName}"

    class Meta:
        model = Boec
        fields = ('id', 'fullName')
        read_only_fields = ('id', 'fullName')


class BoecSerializer(serializers.ModelSerializer):
    """serializer for boec objects"""
    seasons = SeasonSerializer(many=True, read_only=True)
    fullName = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        return f"{obj.lastName} {obj.firstName} {obj.middleName}"

    class Meta:
        model = Boec
        fields = ('id', 'firstName', 'lastName',
                  'middleName', 'DOB', 'seasons', 'fullName')
        read_only_fields = ('id', 'fullName', 'seasons')


class BrigadeSerializer(serializers.ModelSerializer):
    """serializer for brigade objects"""
    boec_count = serializers.SerializerMethodField('get_boec_count')

    def get_boec_count(self, obj):
        return obj.boec.count()

    boec = BoecSerializer(many=True, read_only=True)

    class Meta:
        model = Brigade
        fields = ('id', 'title', 'shtab', 'area', 'DOB', 'boec', 'boec_count')
        read_only_fields = ('id', 'boec_count',)
