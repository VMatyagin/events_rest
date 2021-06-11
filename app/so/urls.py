from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter

from so import views

router = SimpleRouter()

router.register('shtab', views.ShtabViewSet)
router.register('area', views.AreaViewSet)
router.register('boec', views.BoecViewSet)
router.register(r'brigade', views.BrigadeViewSet)
brigade_router = routers.NestedSimpleRouter(
    router, r'brigade', lookup='brigade')
brigade_router.register(r'positions', views.BrigadePositions,
                        basename='brigade-positions')

router.register('season', views.SeasonViewSet)

app_name = 'so'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(brigade_router.urls)),

]
