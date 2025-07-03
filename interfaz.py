import tkinter as tk
from tkinter import messagebox
import auth
import dashboard

def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    if auth.login(usuario, contraseña):
        root.destroy()
        dashboard.mostrar_dashboard()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def registrar():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    try:
        auth.registrar(usuario, contraseña)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
    except Exception:
        messagebox.showerror("Error", "Nombre de usuario ya existente")

def mostrar_login():
    global root, entry_usuario, entry_contraseña
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Usuario").grid(row=0, column=0)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1)

    tk.Label(root, text="Contraseña").grid(row=1, column=0)
    entry_contraseña = tk.Entry(root, show="*")
    entry_contraseña.grid(row=1, column=1)

    tk.Button(root, text="Iniciar sesión", command=login).grid(row=2, column=0)
    tk.Button(root, text="Registrarse", command=registrar).grid(row=2, column=1)

    root.mainloop()