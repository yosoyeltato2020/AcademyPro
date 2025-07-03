import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="+htbgvsKf3gh+",
        database="academias_db"
    )

def crear_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()

def verificar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
