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
    
    conn.close()
    return list(recomendaciones)
