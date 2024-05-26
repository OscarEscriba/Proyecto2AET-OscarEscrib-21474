import sqlite3

def conectar_db():
    return sqlite3.connect("recomendaciones.db")

def obtener_peliculas_relacionadas(pelicula_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = '''
    SELECT p2.id, p2.titulo
    FROM RelacionesPeliculas rp
    JOIN Peliculas p1 ON rp.peliculaId1 = p1.id
    JOIN Peliculas p2 ON rp.peliculaId2 = p2.id
    WHERE p1.id = ?
    UNION
    SELECT p1.id, p1.titulo
    FROM RelacionesPeliculas rp
    JOIN Peliculas p1 ON rp.peliculaId1 = p1.id
    JOIN Peliculas p2 ON rp.peliculaId2 = p2.id
    WHERE p2.id = ?
    '''
    
    cursor.execute(query, (pelicula_id, pelicula_id))
    peliculas_relacionadas = cursor.fetchall()
    
    conn.close()
    return peliculas_relacionadas

def recomendar_peliculas(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = '''
    SELECT peliculaId
    FROM HistorialBusquedas
    WHERE usuarioId = ?
    '''
    
    cursor.execute(query, (usuario_id,))
    historial = cursor.fetchall()
    
    recomendaciones = set()
    for pelicula_id in historial:
        relacionadas = obtener_peliculas_relacionadas(pelicula_id[0])
        for relacionada in relacionadas:
            recomendaciones.add(relacionada)
    
    # Almacenar recomendaciones pasadas
    query_insert = '''
    INSERT INTO RecomendacionesPasadas (usuarioId, peliculaId)
    VALUES (?, ?)
    '''
    for rec in recomendaciones:
        cursor.execute(query_insert, (usuario_id, rec[0]))
    
    conn.commit()
    conn.close()
    return list(recomendaciones)

def obtener_recomendaciones_pasadas(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = '''
    SELECT p.id, p.titulo
    FROM RecomendacionesPasadas rp
    JOIN Peliculas p ON rp.peliculaId = p.id
    WHERE rp.usuarioId = ?
    '''
    
    cursor.execute(query, (usuario_id,))
    recomendaciones_pasadas = cursor.fetchall()
    
    conn.close()
    return recomendaciones_pasadas

def buscar_peliculas_por_titulo(titulo):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = '''
    SELECT id, titulo
    FROM Peliculas
    WHERE titulo LIKE ?
    '''
    
    cursor.execute(query, ('%' + titulo + '%',))
    peliculas = cursor.fetchall()
    
    conn.close()
    return peliculas

def guardar_busqueda_temporal(usuario_id, pelicula_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = '''
    INSERT INTO HistorialBusquedas (usuarioId, peliculaId)
    VALUES (?, ?)
    '''
    
    cursor.execute(query, (usuario_id, pelicula_id))
    conn.commit()
    conn.close()

def borrar_historial(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query_historial = '''
    DELETE FROM HistorialBusquedas
    WHERE usuarioId = ?
    '''
    
    query_recomendaciones = '''
    DELETE FROM RecomendacionesPasadas
    WHERE usuarioId = ?
    '''
    
    cursor.execute(query_historial, (usuario_id,))
    cursor.execute(query_recomendaciones, (usuario_id,))
    conn.commit()
    conn.close()
