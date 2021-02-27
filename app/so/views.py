from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication

from core.models import Boec, Brigade, Season, Shtab, Area
from so import serializers


class ShtabViewSet(viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.ShtabSerializer
    queryset = Shtab.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')


class AreaViewSet(viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.AreaSerializer
    queryset = Area.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by shortTitle objects"""
        return self.queryset.order_by('-shortTitle')


class BoecViewSet(viewsets.ModelViewSet):
    """manage boecs in the database"""
    serializer_class = serializers.BoecSerializer
    queryset = Boec.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by lastName objects"""
        return self.queryset.order_by('-lastName')


class BrigadeViewSet(viewsets.ModelViewSet):
    """manage brigades in the database"""
    serializer_class = serializers.BrigadeSerializer
    queryset = Brigade.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')


class SeasonViewSet(viewsets.ModelViewSet):
    """manage seasons in the database"""
    serializer_class = serializers.SeasonSerializer
    queryset = Season.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return objects"""
        return self.queryset
