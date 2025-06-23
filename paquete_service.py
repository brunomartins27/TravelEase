import sqlite3
from db import crear_conexion

def cargar_paquetes_iniciales():
    iniciales = [
        ("Bariloche", "3 días con hotel 4★", 120000),
        ("Mendoza", "Tour de vinos y hotel boutique", 95000),
        ("Ushuaia", "Excursiones de nieve + hospedaje", 150000)
    ]
    conn = crear_conexion()
    c = conn.cursor()
    for destino, desc, precio in iniciales:
        c.execute("SELECT id FROM paquetes WHERE destino=?", (destino,))
        if not c.fetchone():
            c.execute(
                "INSERT INTO paquetes (destino, descripcion, precio) VALUES (?,?,?)",
                (destino, desc, precio)
            )
    conn.commit()
    conn.close()

def obtener_paquetes_disponibles():
    conn = crear_conexion()
    c = conn.cursor()
    c.execute("SELECT id, destino, descripcion, precio FROM paquetes WHERE disponible=1")
    filas = c.fetchall()
    conn.close()
    return filas

def buscar_paquetes_por_destino(destino):
    conn = crear_conexion()
    c = conn.cursor()
    c.execute(
        "SELECT id, destino, descripcion, precio FROM paquetes WHERE destino LIKE ? AND disponible=1",
        (f"%{destino}%",)
    )
    filas = c.fetchall()
    conn.close()
    return filas
