from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Boec, Shtab, Area
from so import serializers


class ShtabViewSet(viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.ShtabSerializer
    queryset = Shtab.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')


class AreaViewSet(viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.AreaSerializer
    queryset = Area.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by shortTitle objects"""
        return self.queryset.order_by('-shortTitle')


class BoecViewSet(viewsets.ModelViewSet):
    """manage boecs in the database"""
    serializer_class = serializers.BoecSerializer
    queryset = Boec.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by lastName objects"""
        return self.queryset.order_by('-lastName')
