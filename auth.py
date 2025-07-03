import db

def login(usuario, contraseña):
    return db.verificar_usuario(usuario, contraseña)

def registrar(usuario, contraseña):
    return db.crear_usuario(usuario, contraseña)