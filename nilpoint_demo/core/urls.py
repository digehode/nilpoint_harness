from django.urls import path

from .views import HomeView, LoginView, NewUserView, LogoutView, GameLaunchView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("newuser", NewUserView.as_view(), name="newuser"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("game/<slug:nilpoint_slug>", GameLaunchView.as_view(), name="launch"),
]
