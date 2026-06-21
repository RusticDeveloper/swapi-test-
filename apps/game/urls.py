from django.urls import path

from . import views

urlpatterns = [
    # El Tablero de Batalla principal
    path("jugar/", views.vista_juego, name="juego"),
    # Enciclopedia de personajes (Ver mazo/colección)
    path("personajes/", views.vista_personajes, name="personajes"),
    # Endpoint backend: JavaScript llamará aquí para descargar las cartas
    path("juego/api/mazo/", views.api_obtener_mazo, name="api_mazo"),
]
