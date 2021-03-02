from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication
from rest_framework import filters

from reversion.views import RevisionMixin

from core.models import Boec, Brigade, Season, Shtab, Area
from so import serializers


class ShtabViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.ShtabSerializer
    queryset = Shtab.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')


class AreaViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.AreaSerializer
    queryset = Area.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by shortTitle objects"""
        return self.queryset.order_by('-shortTitle')


class BoecViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage boecs in the database"""
    queryset = Boec.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('lastName', 'firstName')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoecShortSerializer
        return serializers.BoecSerializer

    def get_queryset(self):
        """Return ordered by id objects"""
        queryset = self.queryset.order_by('-id')

        brigadeId = self.request.query_params.get('brigadeId', None)
        if brigadeId is not None:
            queryset = queryset.filter(brigades=brigadeId)
        return queryset


class BrigadeViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage brigades in the database"""
    queryset = Brigade.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BrigadeShortSerializer
        return serializers.BrigadeSerializer

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-title')


class SeasonViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage seasons in the database"""
    serializer_class = serializers.SeasonSerializer
    queryset = Season.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-year')
