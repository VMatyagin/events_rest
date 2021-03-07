from django.urls import path, include
from rest_framework.routers import SimpleRouter

from event import views

router = SimpleRouter()

router.register('orders', views.EventOrdersViewSet)
router.register('', views.EventViewSet)

app_name = 'event'

urlpatterns = [
    path('', include(router.urls))
]
