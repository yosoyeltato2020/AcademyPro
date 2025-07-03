import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import date, timedelta

def mostrar_dashboard():
    global academias 
    conn = db.conectar()
    cursor = conn.cursor()

    def obtener_academias():
        cursor.execute("SELECT id, nombre FROM academias")
        return cursor.fetchall()

    def cargar_alumnos(academia_id):
        cursor.execute("SELECT nombre, email, fecha_fin FROM alumnos WHERE academia_id = %s", (academia_id,))
        return cursor.fetchall()

    def registrar_academia():
        nombre = entry_nombre_academia.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        cursor.execute("INSERT INTO academias (nombre, direccion, telefono) VALUES (%s, %s, %s)", 
                    (nombre, direccion, telefono))
        conn.commit()
        cargar_lista_academias()

    def registrar_alumno():
        nombre = entry_nombre_alumno.get()
        email = entry_email.get()
        fecha_fin = entry_fecha_fin.get()
        idx = combo_academias.current()
        if idx < 0:
            messagebox.showwarning("Academia", "Selecciona una academia")
            return
        academia_id = academias[idx][0]
        cursor.execute("INSERT INTO alumnos (nombre, email, fecha_fin, academia_id) VALUES (%s, %s, %s, %s)",
                    (nombre, email, fecha_fin, academia_id))
        conn.commit()
        mostrar_alumnos()

    def cargar_lista_academias():
        academias = obtener_academias()
        combo_academias['values'] = [a[1] for a in academias]

    def mostrar_alumnos(*args):
        lista_alumnos.delete(*lista_alumnos.get_children())
        idx = combo_academias.current()
        if idx >= 0:
            alumnos = cargar_alumnos(academias[idx][0])
            for alum in alumnos:
                lista_alumnos.insert('', tk.END, values=alum)

    def mostrar_seguimiento():
        meses = int(combo_meses.get())
        fecha_limite = date.today() - timedelta(days=meses*30)
        cursor.execute("SELECT nombre FROM alumnos WHERE fecha_fin <= %s", (fecha_limite,))
        resultados = cursor.fetchall()
        if resultados:
            nombres = "\n".join(r[0] for r in resultados)
            messagebox.showinfo("Seguimiento", f"{len(resultados)} alumno(s):\n{nombres}")
        else:
            messagebox.showinfo("Seguimiento", "No hay alumnos con ese plazo.")

    # INTERFAZ
    root = tk.Tk()
    root.title("Panel Principal")

    # Academias
    tk.Label(root, text="Nombre academia").grid(row=0, column=0)
    entry_nombre_academia = tk.Entry(root)
    entry_nombre_academia.grid(row=0, column=1)

    tk.Label(root, text="Dirección").grid(row=1, column=0)
    entry_direccion = tk.Entry(root)
    entry_direccion.grid(row=1, column=1)

    tk.Label(root, text="Teléfono").grid(row=2, column=0)
    entry_telefono = tk.Entry(root)
    entry_telefono.grid(row=2, column=1)

    tk.Button(root, text="Registrar academia", command=registrar_academia).grid(row=3, column=0, columnspan=2)

    # Selector de academia
    tk.Label(root, text="Academia").grid(row=4, column=0)
    combo_academias = ttk.Combobox(root, state="readonly")
    combo_academias.grid(row=4, column=1)
    combo_academias.bind("<<ComboboxSelected>>", mostrar_alumnos)

    # Lista alumnos
    lista_alumnos = ttk.Treeview(root, columns=("Nombre", "Email", "Fecha Fin"), show="headings")
    for col in ("Nombre", "Email", "Fecha Fin"):
        lista_alumnos.heading(col, text=col)
    lista_alumnos.grid(row=5, column=0, columnspan=2)

    # Registro alumnos
    tk.Label(root, text="Nombre alumno").grid(row=6, column=0)
    entry_nombre_alumno = tk.Entry(root)
    entry_nombre_alumno.grid(row=6, column=1)

    tk.Label(root, text="Email").grid(row=7, column=0)
    entry_email = tk.Entry(root)
    entry_email.grid(row=7, column=1)

    tk.Label(root, text="Fecha fin (YYYY-MM-DD)").grid(row=8, column=0)
    entry_fecha_fin = tk.Entry(root)
    entry_fecha_fin.grid(row=8, column=1)

    tk.Button(root, text="Registrar alumno", command=registrar_alumno).grid(row=9, column=0, columnspan=2)

    # Seguimiento
    tk.Label(root, text="Seguimiento (meses)").grid(row=10, column=0)
    combo_meses = ttk.Combobox(root, state="readonly", values=["3", "6", "9"])
    combo_meses.grid(row=10, column=1)
    tk.Button(root, text="Ver seguimiento", command=mostrar_seguimiento).grid(row=11, column=0, columnspan=2)

    # Carga inicial
    cargar_lista_academias()

    root.mainloop()
