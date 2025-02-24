from django.urls import path
from telex.views import integration_json, tick

urlpatterns = [
    path("integration.json", integration_json, name="integration_json"),
    path("tick", tick, name="tick"),
]
