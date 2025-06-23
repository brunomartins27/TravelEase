import unittest
import os
from db import inicializar_bd
from usuario_service import registrar_usuario
from paquete_service import cargar_paquetes_iniciales, obtener_paquetes_disponibles
from reserva_service import crear_reserva, obtener_reservas_por_usuario, cancelar_reserva

class TestReservaService(unittest.TestCase):
    def setUp(self):
        # Reinicia la base de datos antes de cada prueba
        if os.path.exists("travelease.db"):
            os.remove("travelease.db")
        inicializar_bd()
        cargar_paquetes_iniciales()
        registrar_usuario("TestRes", "res@mail.com", "1234")

    def test_crear_y_listar_reserva(self):
        paquetes = obtener_paquetes_disponibles()
        self.assertTrue(paquetes)
        pkg_id = paquetes[0][0]

        # Creamos una reserva fresca aquí
        ok = crear_reserva(1, pkg_id)
        self.assertTrue(ok)

        reservas = obtener_reservas_por_usuario(1)
        self.assertEqual(len(reservas), 1)
        # El segundo campo es el destino
        self.assertEqual(reservas[0][1], paquetes[0][1])

    def test_cancelar_reserva(self):
        paquetes = obtener_paquetes_disponibles()
        self.assertTrue(paquetes)
        pkg_id = paquetes[0][0]

        # Creamos y luego cancelamos
        crear_reserva(1, pkg_id)
        reservas = obtener_reservas_por_usuario(1)
        self.assertEqual(len(reservas), 1)

        res_id = reservas[0][0]
        ok = cancelar_reserva(res_id)
        self.assertTrue(ok)

        reservas2 = obtener_reservas_por_usuario(1)
        self.assertEqual(len(reservas2), 0)

if __name__ == "__main__":
    unittest.main()
