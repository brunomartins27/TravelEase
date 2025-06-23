import sqlite3

def crear_conexion():
    return sqlite3.connect("travelease.db")

def inicializar_bd():
    conn = crear_conexion()
    cursor = conn.cursor()

 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destino TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            disponible INTEGER DEFAULT 1
        )
    """)

 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            paquete_id INTEGER NOT NULL,
            fecha_reserva TEXT NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(paquete_id) REFERENCES paquetes(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_bd()
    print("Base de datos inicializada correctamente.")
