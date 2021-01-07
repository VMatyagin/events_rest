from django.urls import path, include
from rest_framework.routers import SimpleRouter

from so import views

router = SimpleRouter()

router.register('shtab', views.ShtabViewSet)
router.register('area', views.AreaViewSet)

app_name = 'so'

urlpatterns = [
    path('', include(router.urls))
]
