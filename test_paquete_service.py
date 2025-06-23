import unittest
import os
from db import inicializar_bd
from paquete_service import cargar_paquetes_iniciales, obtener_paquetes_disponibles, buscar_paquetes_por_destino

class TestPaqueteService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists("travelease.db"):
            os.remove("travelease.db")
        inicializar_bd()
        cargar_paquetes_iniciales()

    def test_listado_inicial(self):
        paquetes = obtener_paquetes_disponibles()
        self.assertTrue(len(paquetes) >= 3)
        destinos = [p[1] for p in paquetes]
        self.assertIn("Bariloche", destinos)
        self.assertIn("Mendoza", destinos)

    def test_buscar_destino(self):
        resultados = buscar_paquetes_por_destino("Mendo")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0][1], "Mendoza")

if __name__ == "__main__":
    unittest.main()
