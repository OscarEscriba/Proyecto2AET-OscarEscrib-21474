import tkinter as tk
from tkinter import ttk, messagebox
from recomendador import recomendar_peliculas, buscar_peliculas_por_titulo, guardar_busqueda_temporal, agregar_usuario, borrar_historial
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

def actualizar_usuarios():
    usuarios = obtener_usuarios()
    usuario_combobox['values'] = [f"{u[0]} - {u[1]}" for u in usuarios]
    usuario_combobox.set("Seleccione un usuario")

def mostrar_recomendaciones():
    usuario_id = int(usuario_combobox.get().split()[0])
    recomendaciones = recomendar_peliculas(usuario_id)
    recomendaciones_text.delete('1.0', tk.END)
    for rec in recomendaciones:
        recomendaciones_text.insert(tk.END, f"{rec[1]}\n")

def realizar_busqueda():
    usuario_id = int(usuario_combobox.get().split()[0])
    titulo_busqueda = busqueda_entry.get()
    resultados = buscar_peliculas_por_titulo(titulo_busqueda)
    resultados_listbox.delete(0, tk.END)
    for res in resultados:
        resultados_listbox.insert(tk.END, f"{res[0]} - {res[1]}")
    if resultados:
        guardar_busqueda_temporal(usuario_id, resultados[0][0])

def registrar_usuario():
    nombre = nuevo_usuario_entry.get()
    if nombre:
        agregar_usuario(nombre)
        actualizar_usuarios()
        nuevo_usuario_entry.delete(0, tk.END)
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
    else:
        messagebox.showwarning("Registro", "Debe ingresar un nombre.")

def limpiar_historial():
    usuario_id = int(usuario_combobox.get().split()[0])
    borrar_historial(usuario_id)
    messagebox.showinfo("Historial", "Historial de recomendaciones borrado exitosamente.")

app = tk.Tk()
app.title("Sistema de Recomendaciones de Películas")

# Combobox de Usuarios
usuarios = obtener_usuarios()
usuario_combobox = ttk.Combobox(app, values=[f"{u[0]} - {u[1]}" for u in usuarios])
usuario_combobox.grid(row=0, column=1, padx=10, pady=10)
usuario_combobox.set("Seleccione un usuario")

# Campo de búsqueda
busqueda_label = tk.Label(app, text="Buscar película:")
busqueda_label.grid(row=1, column=0, padx=10, pady=10)
busqueda_entry = tk.Entry(app)
busqueda_entry.grid(row=1, column=1, padx=10, pady=10)

# Botón para realizar búsqueda
buscar_button = tk.Button(app, text="Buscar", command=realizar_busqueda)
buscar_button.grid(row=1, column=2, padx=10, pady=10)

# Listbox para mostrar resultados de búsqueda
resultados_listbox = tk.Listbox(app, width=50, height=10)
resultados_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Botón para mostrar recomendaciones
recomendar_button = tk.Button(app, text="Mostrar Recomendaciones", command=mostrar_recomendaciones)
recomendar_button.grid(row=3, column=1, padx=10, pady=10)

# Área de texto para mostrar recomendaciones
recomendaciones_text = tk.Text(app, width=50, height=10)
recomendaciones_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Campo para nuevo usuario
nuevo_usuario_label = tk.Label(app, text="Nuevo usuario:")
nuevo_usuario_label.grid(row=5, column=0, padx=10, pady=10)
nuevo_usuario_entry = tk.Entry(app)
nuevo_usuario_entry.grid(row=5, column=1, padx=10, pady=10)

# Botón para registrar nuevo usuario
registrar_button = tk.Button(app, text="Registrar", command=registrar_usuario)
registrar_button.grid(row=5, column=2, padx=10, pady=10)

# Botón para limpiar historial de recomendaciones
limpiar_button = tk.Button(app, text="Limpiar Historial", command=limpiar_historial)
limpiar_button.grid(row=6, column=1, padx=10, pady=10)

app.mainloop()

