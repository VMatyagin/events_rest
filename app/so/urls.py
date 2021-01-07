from django.urls import path, include
from rest_framework.routers import SimpleRouter

from so import views

router = SimpleRouter()

router.register('shtab', views.ShtabViewSet)
router.register('area', views.AreaViewSet)
router.register('boec', views.BoecViewSet)
router.register('brigade', views.BrigadeViewSet)

app_name = 'so'

urlpatterns = [
    path('', include(router.urls))
]
