from django.urls import path

from .views import HomeView, LoginView, NewUserView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("newuser", NewUserView.as_view(), name="newuser"),
    path("login", LoginView.as_view(), name="login"),
]
