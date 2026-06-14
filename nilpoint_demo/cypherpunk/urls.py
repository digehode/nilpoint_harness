from django.urls import path
from .views import DebugView

app_name = "cypherpunkgame"
urlpatterns = [
    path("", DebugView.as_view(), name="dispatch"),
]
