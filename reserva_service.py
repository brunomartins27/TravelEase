from db import crear_conexion
from datetime import datetime

def crear_reserva(usuario_id, paquete_id):
    conn = crear_conexion()
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO reservas (usuario_id, paquete_id, fecha_reserva) VALUES (?, ?, ?)",
        (usuario_id, paquete_id, fecha)
    )
    conn.commit()
    conn.close()
    return True

def crear_reservas_multiples(reservas):
    conn = crear_conexion()
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for usuario_id, paquete_id in reservas:
        c.execute(
            "INSERT INTO reservas (usuario_id, paquete_id, fecha_reserva) VALUES (?, ?, ?)",
            (usuario_id, paquete_id, fecha)
        )
    conn.commit()
    conn.close()
    return True

def obtener_reservas_por_usuario(usuario_id):
    conn = crear_conexion()
    c = conn.cursor()
    c.execute("""
        SELECT r.id, p.destino, p.precio, r.fecha_reserva
        FROM reservas r
        JOIN paquetes p ON r.paquete_id = p.id
        WHERE r.usuario_id = ?
    """, (usuario_id,))
    filas = c.fetchall()
    conn.close()
    return filas

def cancelar_reserva(reserva_id):
    conn = crear_conexion()
    c = conn.cursor()
    c.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()
    return True
