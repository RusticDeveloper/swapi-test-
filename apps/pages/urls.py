from django.urls import path

from . import views

urlpatterns = [
    # Ruta raíz pura: La Landing Page con reglas y créditos
    path("", views.home_landing, name="home"),
    # Otras páginas del menú superior
    path("rankings/", views.vista_rankings, name="rankings"),
    path("acerca-de/", views.vista_acerca_de, name="acerca_de"),
]
