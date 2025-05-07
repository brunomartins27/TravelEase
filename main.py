from usuario import crear_usuario, autenticar_usuario
from paquete import buscar_paquetes
from reserva import reservar_paquete, realizar_pago

# Creación y autenticación del usuario
usuario = crear_usuario("Juan Perez", "juan@example.com", "password123")
print("Usuario creado:", usuario.nombre)

autenticado = autenticar_usuario("juan@example.com", "password123")
print("Autenticación exitosa" if autenticado else "Fallo en la autenticación")

# Búsqueda de paquetes turísticos
destino_busqueda = "Bariloche"
paquetes = buscar_paquetes(destino_busqueda)

if paquetes:
    print(f"Paquetes disponibles para {destino_busqueda}:")
    for p in paquetes:
        print(f"- {p.destino}: ${p.precio}")
else:
    print("No hay paquetes disponibles para este destino.")

# Reserva y pago
reserva = reservar_paquete(usuario, destino_busqueda)

if reserva:
    print(f"Reserva realizada para {reserva.paquete.destino}. Precio: ${reserva.paquete.precio}")
    pago_realizado = realizar_pago(reserva, "tarjeta")
    if pago_realizado:
        print("Pago realizado con éxito. Reserva confirmada.")
    else:
        print("El pago no pudo ser procesado.")
else:
    print("La reserva no pudo realizarse. Paquete no disponible.")
