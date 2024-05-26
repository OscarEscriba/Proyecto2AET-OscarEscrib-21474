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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RecomendacionesPasadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuarioId INTEGER,
        peliculaId INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuarioId) REFERENCES Usuarios(id),
        FOREIGN KEY (peliculaId) REFERENCES Peliculas(id)
    )
    ''')

    conn.commit()
    conn.close()

def insertar_datos_iniciales():
    conn = conectar_db()
    cursor = conn.cursor()

    peliculas = [
        ('The Little Mermaid', 'Animation', 'A curious mermaid princess dreams of life on land and falls in love with a human prince, defying her father\'s wishes and making a deal with a sea witch.'),
        ('Mulan', 'Animation', 'A young Chinese maiden disguises herself as a male warrior to save her father and her country from an invading army.'),
        ('Toy Story', 'Animation', 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.'),
        ('Finding Nemo', 'Animation', 'After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home.'),
        ('Zootopia', 'Animation', 'In a city of anthropomorphic animals, a rookie bunny cop and a cynical con artist fox must work together to uncover a conspiracy.'),
        ('The Incredibles', 'Animation', 'A family of undercover superheroes, while trying to live the quiet suburban life, are forced into action to save the world.'),
        ('Up', 'Animation', 'Seventy-eight year old Carl Fredricksen travels to Paradise Falls in his home equipped with balloons, inadvertently taking a young stowaway.'),
        ('Monsters, Inc.', 'Animation', 'In order to power the city, monsters have to scare children so that they scream. However, the children are toxic to the monsters, and after a child gets through, two monsters realize things may not be what they think.'),
        ('Ratatouille', 'Animation', 'A rat who can cook makes an unusual alliance with a young kitchen worker at a famous Paris restaurant.'),
        ('Wall-E', 'Animation', 'In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.'),
        ('Brave', 'Animation', 'Determined to make her own path in life, Princess Merida defies a custom that brings chaos to her kingdom. Granted one wish, Merida must rely on her bravery and her archery skills to undo a beastly curse.'),
        ('Tangled', 'Animation', 'The magically long-haired Rapunzel has spent her entire life in a tower, but now that a runaway thief has stumbled upon her, she is about to discover the world for the first time, and who she really is.'),
        ('Big Hero 6', 'Animation', 'A special bond develops between plus-sized inflatable robot Baymax and prodigy Hiro Hamada, who team up with a group of friends to form a band of high-tech heroes.'),
        ('Coco', 'Animation', 'Aspiring musician Miguel, confronted with his family\'s ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.'),
        ('The Princess and the Frog', 'Animation', 'A waitress, desperate to fulfill her dreams as a restaurant owner, is set on a journey to turn a frog prince back into a human being, but she has to face the same problem after she kisses him.'),
        ('Snow White and the Seven Dwarfs', 'Animation', 'Snow White, pursued by a jealous queen, hides with the Dwarfs, but the queen learns of this and prepares to feed her a poison apple.'),
        ('Alice in Wonderland', 'Animation', 'Alice stumbles into the world of Wonderland. Will she get home? Not if the Queen of Hearts has her way.'),
        ('Peter Pan', 'Animation', 'Wendy and her brothers are whisked away to the magical world of Neverland with the hero of their stories, Peter Pan.'),
        ('Tarzan', 'Animation', 'A man raised by gorillas must decide where he really belongs when he discovers he is a human.'),
        ('Hercules', 'Animation', 'The son of Zeus and Hera is stripped of his immortality as an infant and must become a true hero in order to reclaim it.')
    ]

    cursor.executemany('INSERT INTO Peliculas (titulo, genero, sinopsis) VALUES (?, ?, ?)', peliculas)

    usuarios = [
        ('Juan Perez',),
        ('Ana Gomez',)
    ]
    cursor.executemany('INSERT INTO Usuarios (nombre) VALUES (?)', usuarios)

    historial_busquedas = [
        (1, 1),  # Juan Perez buscó The Little Mermaid
        (2, 2)   # Ana Gomez buscó Mulan
    ]
    cursor.executemany('INSERT INTO HistorialBusquedas (usuarioId, peliculaId) VALUES (?, ?)', historial_busquedas)

    relaciones_peliculas = [
        (1, 2),  # Relación entre The Little Mermaid y Mulan
        (1, 3),  # Relación entre The Little Mermaid y Toy Story
        (2, 4),  # Relación entre Mulan y Finding Nemo
        (3, 5),  # Relación entre Toy Story y Zootopia
        (4, 6),  # Relación entre Finding Nemo y The Incredibles
        (5, 7),  # Relación entre Zootopia y Up
        (6, 8),  # Relación entre The Incredibles y Monsters, Inc.
        (7, 9),  # Relación entre Up y Ratatouille
        (8, 10), # Relación entre Monsters, Inc. y Wall-E
        (9, 11), # Relación entre Ratatouille y Brave
        (10, 12),# Relación entre Wall-E y Tangled
        (11, 13),# Relación entre Brave y Big Hero 6
        (12, 14),# Relación entre Tangled y Coco
        (13, 15),# Relación entre Big Hero 6 y The Princess and the Frog
        (14, 16),# Relación entre Coco y Snow White and the Seven Dwarfs
        (15, 17),# Relación entre The Princess and the Frog y Alice in Wonderland
        (16, 18),# Relación entre Snow White and the Seven Dwarfs y Peter Pan
        (17, 19),# Relación entre Alice in Wonderland y Tarzan
        (18, 20),# Relación entre Peter Pan y Hercules
        (19, 1), # Relación entre Tarzan y The Little Mermaid
        (20, 2)  # Relación entre Hercules y Mulan
    ]
    cursor.executemany('INSERT INTO RelacionesPeliculas (peliculaId1, peliculaId2) VALUES (?, ?)', relaciones_peliculas)

    conn.commit()
    conn.close()

# Crear tablas y datos iniciales
crear_tablas()
insertar_datos_iniciales()