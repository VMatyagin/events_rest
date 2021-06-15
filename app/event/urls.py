from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from event import views

router = SimpleRouter()

router.register(r'', views.EventViewSet)
event_router = routers.NestedSimpleRouter(
    router, r'', lookup='')
event_router.register(r'volonteers', views.EventVolonteers,
                      basename='event-volonteers')
event_router.register(r'organizers', views.EventOrganizers,
                      basename='event-organizers')
app_name = 'event'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_router.urls)),

]
