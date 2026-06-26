import random
import re

import requests
from django.http import JsonResponse
from django.shortcuts import render


# --- 1. FUNCIÓN AYUDANTE PARA LIMPIAR EL KI ---
def limpiar_y_calcular_ki(ki_texto):
    if not ki_texto or str(ki_texto).strip().lower() in ["unknown", "none", "?", ""]:
        return -1

    ki_str = str(ki_texto).lower().replace(",", "").strip()

    if "googolplex" in ki_str:
        return 10**100

    # Diccionario de multiplicadores
    multiplicadores = {
        "septillion": 10**24,
        "sextillion": 10**21,
        "quintillion": 10**18,
        "quadrillion": 10**15,
        "trillion": 10**12,
        "billion": 10**9,
        "million": 10**6,
    }

    tiene_palabra = False
    factor = 1

    # Revisar si tiene alguna palabra de escala
    for palabra, valor in multiplicadores.items():
        if palabra in ki_str:
            tiene_palabra = True
            factor = valor
            break

    # Si es solo un número (ej: "42.000" o "1.500"), el punto es de miles, hay que quitarlo
    if not tiene_palabra:
        ki_str = ki_str.replace(".", "")

    # Extraer los números
    match = re.search(r"([\d\.]+)", ki_str)
    if not match:
        return -1

    try:
        valor_base = float(match.group(1))
    except ValueError:
        return -1

    # Retornar el valor base multiplicado por su escala (si no tiene escala, factor es 1)
    return valor_base * factor


# --- 2. ENDPOINT PRINCIPAL DEL JUEGO ---
def api_obtener_mazo(request):
    """Endpoint Backend: Descarga y pre-calcula los stats exactos para el TCG."""
    url = "https://dragonball-api.com/api/characters?page=1&limit=80"  # Ampliamos el límite para asegurar que entren deidades
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code != 200:
            return JsonResponse(
                {"status": "error", "message": "API externa caída"}, status=500
            )

        datos = respuesta.json()
        personajes = datos.get("items", [])
        mazo_procesado = []

        for p in personajes:
            # Regla: Tomar maxKi (Ki total), si no hay, tomar ki base
            ki_texto = (
                p.get("maxKi")
                if p.get("maxKi") and p.get("maxKi") != "0"
                else p.get("ki")
            )

            # Llamamos a nuestra nueva función inteligente
            ki_num = limpiar_y_calcular_ki(ki_texto)

            # Asignación de ATK y Costo bajo tus nuevas reglas
            if ki_num == -1:  # Desconocido
                atk, costo, tipo_ki = 0, 4, "unknown"
            elif ki_num == 0:
                atk, costo, tipo_ki = 0, 1, "zero"
            elif ki_num <= 5_000:
                atk, costo, tipo_ki = 400, 1, "normal"
            elif ki_num <= 50_000:
                atk, costo, tipo_ki = 1000, 2, "normal"
            elif ki_num <= 500_000:
                atk, costo, tipo_ki = 1800, 3, "normal"
            elif ki_num <= 5_000_000:
                atk, costo, tipo_ki = 2600, 4, "normal"
            elif ki_num <= 50_000_000:
                atk, costo, tipo_ki = 3400, 5, "normal"
            elif ki_num <= 500_000_000:
                atk, costo, tipo_ki = 4500, 6, "normal"
            else:
                # Escala de Dioses (500M hasta Googolplex -> ATK de 5,000 a 10,000)
                costo, tipo_ki = 7, "dios"
                if ki_num >= 10**100:
                    atk = 10000  # Googolplex
                elif ki_num >= 10**24:
                    atk = 9000  # Septillones
                elif ki_num >= 10**21:
                    atk = 8500  # Sextillones
                elif ki_num >= 10**18:
                    atk = 8000  # Quintillones
                elif ki_num >= 10**12:
                    atk = 7000  # Trillones
                else:
                    atk = 6000  # Billones

            mazo_procesado.append(
                {
                    "id": p.get("id"),
                    "name": p.get("name"),
                    "image": p.get("image"),
                    "atk": atk,
                    "costo": costo,
                    "tipo_ki": tipo_ki,
                    "ki_original": ki_texto,
                }
            )

        random.shuffle(mazo_procesado)
        return JsonResponse({"status": "success", "cartas": mazo_procesado}, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


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
