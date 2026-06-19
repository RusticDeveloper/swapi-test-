# apps/cartas/urls.py
from django.urls import path

from .views import probar_api_dbz

urlpatterns = [
    path("probar-api/", probar_api_dbz, name="probar_api_dbz"),
]
