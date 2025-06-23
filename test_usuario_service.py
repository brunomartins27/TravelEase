import unittest
import os
from db import inicializar_bd
from usuario_service import registrar_usuario, autenticar_usuario

class TestUsuarioService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reinicia la BD antes de todas las pruebas
        if os.path.exists("travelease.db"):
            os.remove("travelease.db")
        inicializar_bd()

    def test_registrar_autenticar(self):
        ok, msg = registrar_usuario("Ana", "ana@mail.com", "pass123")
        self.assertTrue(ok)
        self.assertEqual(msg, "Usuario registrado correctamente.")

        ok2, data = autenticar_usuario("ana@mail.com", "pass123")
        self.assertTrue(ok2)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["nombre"], "Ana")

    def test_registro_duplicado(self):
        # El mismo email no puede volver a registrarse
        ok, msg = registrar_usuario("Ana2", "ana@mail.com", "otra")
        self.assertFalse(ok)
        self.assertIn("registrado", msg)

if __name__ == "__main__":
    unittest.main()
