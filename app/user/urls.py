from django.urls import include, path
from rest_framework.routers import SimpleRouter
from user import views

app_name = "user"

router = SimpleRouter()

urlpatterns = [
    path("me/", views.ManangeUserView.as_view(), name="me"),
    path("activity/", views.ActivityView.as_view({"get": "retrieve"}), name="activity"),
    path(
        "activity/markAsRead",
        views.ActivityView.as_view({"post": "markAsRead"}),
        name="activity",
    ),
]
