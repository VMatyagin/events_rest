from datetime import datetime, timezone
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication
from rest_framework import filters
import logging
from django.utils.translation import ugettext_lazy as _

from reversion.views import RevisionMixin

from core.models import Boec, Brigade, Position, Season, Shtab, Area
from so import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    pass


class ShtabViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.ShtabSerializer
    queryset = Shtab.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('title')


class AreaViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage shtabs in the database"""
    serializer_class = serializers.AreaSerializer
    queryset = Area.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return ordered by shortTitle objects"""
        return self.queryset


class BoecViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage boecs in the database"""
    queryset = Boec.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('^lastName', )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoecInfoSerializer
        return serializers.BoecSerializer

    def get_queryset(self):
        """Return ordered by id objects"""
        queryset = self.queryset.order_by('lastName')

        brigadeId = self.request.query_params.get('brigadeId', None)
        if brigadeId is not None:
            queryset = queryset.filter(brigades=brigadeId)
        return queryset

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='seasons', url_name='seasons',
            authentication_classes=(VKAuthentication,))
    def handleBoecSeasons(self, request, pk):
        seasons = Season.objects.filter(boec=pk)
        """get users list"""
        serializer = serializers.SeasonSerializer(
            seasons, many=True, fields=('id', 'year', 'brigade'))
        return Response(serializer.data)


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
        return self.queryset.order_by('title')


logger = logging.getLogger(__name__)


class BrigadePositions(RevisionMixin, CreateListRetrieveViewSet):
    serializer_class = serializers.PositionSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        return Position.objects.filter(brigade=self.kwargs['brigade_pk'], toDate=None)

    def perform_create(self, serializer):
        try:
            brigade = Brigade.objects.get(id=self.kwargs['brigade_pk'])
        except (Brigade.DoesNotExist, ValidationError):
            msg = _('Invalid brigade.')
            raise ValidationError(
                {'error': msg}, code='validation')

        serializer.save(brigade=brigade)

    @action(methods=['post'], detail=True,
            permission_classes=(IsAuthenticated, ),
            authentication_classes=(VKAuthentication,),
            url_path='remove', url_name='remove')
    def removeBrigadePosition(self, request, pk, brigade_pk):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data={'toDate': datetime.now()}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class BrigadeSeasons(RevisionMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SeasonSerializer
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        return Season.objects.filter(brigade=self.kwargs['brigade_pk']).order_by('boec__lastName')

class SeasonViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage seasons in the database"""
    serializer_class = serializers.SeasonSerializer
    queryset = Season.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-year')
