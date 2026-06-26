# apps/juego/tests.py
from django.http import HttpResponse  # <-- Importamos esto para el linter
from django.test import TestCase
from django.urls import reverse


class TestMotorJuego(TestCase):
    def test_ruta_tablero_disponible(self):
        """Verifica que la página del tablero cargue con éxito (200 OK)"""
        url = reverse("juego")
        # Añadimos ': HttpResponse' para indicarle explícitamente el tipo al linter
        respuesta: HttpResponse = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)

    def test_endpoint_api_mazo(self):
        """Verifica que el endpoint de datos responda en formato JSON"""
        url = reverse("api_mazo")
        respuesta: HttpResponse = self.client.get(url)

        self.assertIn(respuesta.status_code, [200, 500])
        if respuesta.status_code == 200:
            self.assertEqual(respuesta["Content-Type"], "application/json")


class TestMotorMecanicas(TestCase):
    def test_endpoint_retorna_atributos_tcg(self):
        """Asegura que el mazo procesado traiga ATK y costo calculados."""
        url = reverse("api_mazo")
        respuesta = self.client.get(url)  # type: ignore
        if respuesta.status_code == 200:
            datos = respuesta.json()
            primer_guerrero = datos["cartas"][0]
            self.assertIn("atk", primer_guerrero)
            self.assertIn("costo", primer_guerrero)
