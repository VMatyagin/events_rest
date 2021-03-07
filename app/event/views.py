from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication
from rest_framework import filters

from reversion.views import RevisionMixin

from core.models import Event, EventOrder
from event import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from so.serializers import BoecShortSerializer


class EventViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage events in the database"""
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )

    filter_backends = [filters.SearchFilter]
    search_fields = ('title', )

    def get_queryset(self):
        """Return ordered by title objects"""
        return self.queryset.order_by('-startDate')

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='toggle', url_name='toggle_visibility')
    def toggle_visibility(self, request, pk=None):
        """Toggle event visibility"""
        event = Event.objects.get(pk=pk)
        event.visibility = not event.visibility
        event.save()

        serializer = self.serializer_class(event, many=False)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='volonteers', url_name='volonteers')
    def get_volonteers(self, request, pk=None):
        """get volonteers list"""
        event = Event.objects.get(pk=pk)

        serializer = BoecShortSerializer(event.volonteer, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='organizers', url_name='organizers')
    def get_organizers(self, request, pk=None):
        """get organizers list"""
        event = Event.objects.get(pk=pk)

        serializer = BoecShortSerializer(event.organizer, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='orders', url_name='orders')
    def get_orders(self, request, pk=None):
        """get orders list"""
        event = Event.objects.get(pk=pk)

        serializer = serializers.OrderSerializer(event.orders, many=True)

        return Response(serializer.data)

class EventOrdersViewSet(RevisionMixin, viewsets.ModelViewSet):
    """manage orders in the database"""
    serializer_class = serializers.OrderSerializer
    queryset = EventOrder.objects.all()
    authentication_classes = (VKAuthentication,)
    permission_classes = (IsAuthenticated, )
    paginator = None
