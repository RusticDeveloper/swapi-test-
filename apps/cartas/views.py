import requests
from django.http import JsonResponse
from django.shortcuts import render


def probar_api_dbz(request):
    # Consumimos el endpoint de la API de Dragon Ball Z para obtener personajes
    url = "https://dragonball-api.com/api/characters?page=1&limit=10"

    try:
        respuesta = requests.get(url)
        datos = respuesta.json()  # Convertimos la respuesta a un diccionario de Python

        # De momento, solo mostraremos los datos crudos en la pantalla para verificar
        return JsonResponse(datos, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": f"No se pudo conectar a la API: {str(e)}"}, status=500
        )
