from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.authentication import VKAuthentication
from rest_framework import filters, status

from reversion.views import RevisionMixin

from core.models import Boec, Brigade, Event, EventOrder
from event import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from so.serializers import BoecInfoSerializer


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

    def handleUsers(self, request, pk, type='volonteer'):
        event = Event.objects.get(pk=pk)
        list = getattr(event, type)
        if request.method == 'POST':
            isRemove = self.request.query_params.get('isRemove')
            if isRemove:
                """delete user from type of event"""
                try:
                    id = request.data['id']
                    boec = Boec.objects.get(id=id)
                    list.remove(boec)
                except (Boec.DoesNotExist, ValidationError):
                    raise status.HTTP_400_BAD_REQUEST
            else:
                """add user to type to event"""
                try:
                    id = request.data['id']
                    boec = Boec.objects.get(id=id)
                    list.add(boec)
                except (Boec.DoesNotExist, ValidationError):
                    raise status.HTTP_400_BAD_REQUEST
        """get users list"""
        serializer = BoecInfoSerializer(list, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'post'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='volonteers', url_name='volonteers')
    def handle_volonteers(self, request, pk=None):
        return self.handleUsers(request=request, pk=pk, type='volonteer')

    @action(methods=['get', 'post'], detail=True, permission_classes=(IsAuthenticated, ),
            url_path='organizers', url_name='organizers')
    def handle_organizers(self, request, pk=None):
        return self.handleUsers(request=request, pk=pk, type='organizer')

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

    def validate_ids(self, id_list, model):
        for id in id_list:
            try:
                model.objects.get(id=id)
            except (model.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def update(self, request, *args, **kwargs):
        if 'brigades_id' in request.data:
            id_list = request.data['brigades_id']

            self.validate_ids(id_list=id_list, model=Brigade)
            instances = []
            for id in id_list:
                obj = Brigade.objects.get(id=id)
                instances.append(obj)
            order = EventOrder.objects.get(id=request.data['id'])
            order.brigades.set(instances)
            order.save()

            del request.data['brigades_id']

        if 'participations' in request.data:
            id_list = list(map(
                lambda x: x['id'], request.data['participations']
            ))

            self.validate_ids(id_list=id_list, model=Boec)
            instances = []
            for id in id_list:
                obj = Boec.objects.get(id=id)
                instances.append(obj)
            order = EventOrder.objects.get(id=request.data['id'])
            order.participations.set(instances)
            order.save()

            del request.data['participations']

        return super().update(request, *args, **kwargs)
