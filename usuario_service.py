import sqlite3
from db import crear_conexion

def registrar_usuario(nombre, email, contraseña):
    try:
        conn = crear_conexion()
        c = conn.cursor()
        c.execute(
            "INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)",
            (nombre, email, contraseña)
        )
        conn.commit()
        conn.close()
        return True, "Usuario registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "El email ya está registrado."

def autenticar_usuario(email, contraseña):
    conn = crear_conexion()
    c = conn.cursor()
    c.execute(
        "SELECT id, nombre FROM usuarios WHERE email=? AND contraseña=?",
        (email, contraseña)
    )
    fila = c.fetchone()
    conn.close()
    if fila:
        return True, {"id": fila[0], "nombre": fila[1]}
    else:
        return False, "Email o contraseña incorrectos."
