class Usuario:
    def __init__(self, nombre, email, contraseña):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña

usuarios_registrados = []

def crear_usuario(nombre, email, contraseña):
    nuevo_usuario = Usuario(nombre, email, contraseña)
    usuarios_registrados.append(nuevo_usuario)
    return nuevo_usuario

def autenticar_usuario(email, contraseña):
    for usuario in usuarios_registrados:
        if usuario.email == email and usuario.contraseña == contraseña:
            return True
    return False
