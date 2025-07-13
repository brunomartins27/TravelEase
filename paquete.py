class Paquete:
    def __init__(self, destino, precio, disponible=True):
        self.destino = destino
        self.precio = precio
        self.disponible = disponible

paquetes_disponibles = [
    Paquete("Bariloche", 120000),
    Paquete("Mendoza", 95000),
    Paquete("Ushuaia", 150000, disponible=False),
    Paquete("Rio de Janeiro", 250000),
    Paquete("San Pablo", 220000),
    Paquete("Frankfurt", 600000)
]

def buscar_paquetes(destino):
    resultados = [p for p in paquetes_disponibles if p.destino.lower() == destino.lower() and p.disponible]
    return resultados
