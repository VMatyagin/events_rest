from django.urls import path
from user import views

app_name = "user"

urlpatterns = [path("me/", views.ManangeUserView.as_view(), name="me")]
