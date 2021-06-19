from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from so import views

router = SimpleRouter()

router.register("shtab", views.ShtabViewSet)
router.register("area", views.AreaViewSet)
router.register("boec", views.BoecViewSet)
router.register(r"brigade", views.BrigadeViewSet)
brigade_router = routers.NestedSimpleRouter(router, r"brigade", lookup="brigade")
brigade_router.register(
    r"positions", views.BrigadePositions, basename="brigade-positions"
)
brigade_router.register(r"seasons", views.BrigadeSeasons, basename="brigade-seasons")
boec_router = routers.NestedSimpleRouter(router, r"boec", lookup="boec")

boec_router.register(r"positions", views.BoecPositions, basename="boec-positions")
boec_router.register(r"seasons", views.BoecSeasons, basename="boec-seasons")

router.register(r"conference", views.ConferenceViewSet)

router.register("season", views.SeasonViewSet)

app_name = "so"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(brigade_router.urls)),
    path("", include(boec_router.urls)),
]
