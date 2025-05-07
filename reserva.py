from paquete import paquetes_disponibles

class Reserva:
    def __init__(self, usuario, paquete):
        self.usuario = usuario
        self.paquete = paquete

reservas_realizadas = []

def reservar_paquete(usuario, destino):
    for paquete in paquetes_disponibles:
        if paquete.destino.lower() == destino.lower() and paquete.disponible:
            nueva_reserva = Reserva(usuario, paquete)
            reservas_realizadas.append(nueva_reserva)
            return nueva_reserva
    return None

def realizar_pago(reserva, metodo_pago):
    if metodo_pago in ["tarjeta", "transferencia"]:
        return True
    return False
