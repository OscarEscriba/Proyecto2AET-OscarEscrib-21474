import tkinter as tk
from tkinter import ttk, messagebox
from recomendador import recomendar_peliculas
from database import conectar_db

def obtener_peliculas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo FROM Peliculas')
    peliculas = cursor.fetchall()
    conn.close()
    return peliculas

def obtener_usuarios():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM Usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def mostrar_recomendaciones():
    usuario_id = int(usuario_combobox.get().split()[0])
    recomendaciones = recomendar_peliculas(usuario_id)
    recomendaciones_text.delete('1.0', tk.END)
    for rec in recomendaciones:
        recomendaciones_text.insert(tk.END, f"{rec[1]}\n")

app = tk.Tk()
app.title("Sistema de Recomendaciones de Películas")

# Combobox de Usuarios
usuarios = obtener_usuarios()
usuario_combobox = ttk.Combobox(app, values=[f"{u[0]} - {u[1]}" for u in usuarios])
usuario_combobox.grid(row=0, column=1, padx=10, pady=10)
usuario_combobox.set("Seleccione un usuario")

# Botón para mostrar recomendaciones
recomendar_button = tk.Button(app, text="Mostrar Recomendaciones", command=mostrar_recomendaciones)
recomendar_button.grid(row=1, column=1, padx=10, pady=10)

# Área de texto para mostrar recomendaciones
recomendaciones_text = tk.Text(app, width=50, height=10)
recomendaciones_text.grid(row=2, column=1, padx=10, pady=10)

app.mainloop()
