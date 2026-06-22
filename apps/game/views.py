import random

import requests
from django.http import JsonResponse
from django.shortcuts import render


def vista_juego(request):
    """
    Tablero de Batalla principal (Interfaz estilo Yu-Gi-Oh!).
    """
    return render(request, "game/tablero.html")


def vista_personajes(request):
    """
    Enciclopedia / Álbum de personajes para ver la colección disponible.
    """
    # Para la enciclopedia, traemos los primeros 20 personajes directo en el backend
    url = "https://dragonball-api.com/api/characters?page=1&limit=20"
    personajes = []

    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            personajes = datos.get("items", [])
    except requests.exceptions.RequestException:
        # Si la API falla, pasamos la lista vacía y la plantilla manejará el error elegantemente
        pass

    return render(request, "juego/personajes.html", {"personajes": personajes})


def api_obtener_mazo(request):
    """
    Endpoint Backend: JavaScript/HTMX llamará aquí de forma interna
    para descargar y mezclar las 35 cartas del mazo de la partida.
    """
    url = "https://dragonball-api.com/api/characters?page=1&limit=35"

    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            personajes = datos.get("items", [])

            # Mezclamos el mazo aleatoriamente para que cada partida sea diferente
            random.shuffle(personajes)

            return JsonResponse({"status": "success", "cartas": personajes}, safe=False)
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No se pudo obtener datos de la API de DBZ",
                },
                status=respuesta.status_code,
            )

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"status": "error", "message": f"Error de conexión: {str(e)}"}, status=500
        )
