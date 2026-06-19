from django.test import TestCase


class TestJuegoDBZ(TestCase):
    def test_logica_combate_basica(self):
        # Simulamos que la vida de un Saiyajin debería ser 100
        vida_goku = 100
        # Forzamos un fallo: decimos que 100 es igual a 999
        self.assertEqual(vida_goku, 999)
