from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from event import views

router = SimpleRouter()

router.register(r'event', views.EventViewSet)

event_router = routers.NestedSimpleRouter(
    router, r'event', lookup='event')

event_router.register(r'participants', views.EventParticipant,
                      basename='event-participants')

event_router.register(r'competitions', views.EventCompetitionListCreate,
                      basename='competitions')


router.register(
    r'competition', views.EventCompetitionRetrieveUpdateDestroy, basename='competition')

event_participants_router = routers.NestedSimpleRouter(
    router, r'competition', lookup='competition')

event_participants_router.register(r'participants', views.EventCompetitionParticipants,
                                   basename='competition-participants')

event_participants_router.register(r'nominations', views.NominationView,
                      basename='competition-nominations')

app_name = 'event'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),
    path('', include(event_participants_router.urls)),
]
