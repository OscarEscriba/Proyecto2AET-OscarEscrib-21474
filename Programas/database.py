import sqlite3

def conectar_db():
    return sqlite3.connect("recomendaciones.db")

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Peliculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        genero TEXT,
        sinopsis TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistorialBusquedas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuarioId INTEGER,
        peliculaId INTEGER,
        FOREIGN KEY (usuarioId) REFERENCES Usuarios(id),
        FOREIGN KEY (peliculaId) REFERENCES Peliculas(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RelacionesPeliculas (
        peliculaId1 INTEGER,
        peliculaId2 INTEGER,
        FOREIGN KEY (peliculaId1) REFERENCES Peliculas(id),
        FOREIGN KEY (peliculaId2) REFERENCES Peliculas(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def insertar_datos_iniciales():
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Insertar datos en la tabla Peliculas
    peliculas = [
        ('Inception', 'Sci-Fi', 'A thief who steals corporate secrets through the use of dream-sharing technology.'),
        ('The Matrix', 'Sci-Fi', 'A computer hacker learns from mysterious rebels about the true nature of his reality.'),
        ('The Godfather', 'Crime', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.')
    ]
    cursor.executemany('INSERT INTO Peliculas (titulo, genero, sinopsis) VALUES (?, ?, ?)', peliculas)
    
    # Insertar datos en la tabla Usuarios
    usuarios = [
        ('Juan Perez',),
        ('Ana Gomez',)
    ]
    cursor.executemany('INSERT INTO Usuarios (nombre) VALUES (?)', usuarios)
    
    # Insertar datos en la tabla HistorialBusquedas
    historial_busquedas = [
        (1, 1),  # Juan Perez buscó Inception
        (2, 2)   # Ana Gomez buscó The Matrix
    ]
    cursor.executemany('INSERT INTO HistorialBusquedas (usuarioId, peliculaId) VALUES (?, ?)', historial_busquedas)
    
    # Insertar datos en la tabla RelacionesPeliculas
    relaciones_peliculas = [
        (1, 2),  # Relación entre Inception y The Matrix
        (2, 3)   # Relación entre The Matrix y The Godfather
    ]
    cursor.executemany('INSERT INTO RelacionesPeliculas (peliculaId1, peliculaId2) VALUES (?, ?)', relaciones_peliculas)
    
    conn.commit()
    conn.close()

# Crear tablas y datos iniciales
crear_tablas()
insertar_datos_iniciales()
