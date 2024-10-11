import sqlite3

# Nombre del fichero de la base de datos
db_name = "fitbot.db"

# Crear las tablas
def create_tables():
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL CHECK (edad >= 0 AND edad <= 120),
        peso INTEGER NOT NULL,
        idioma TEXT NOT NULL        
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tiposRutina (
        id INTEGER,
        infoRutina TEXT NOT NULL,
        rango VARCHAR NOT NULL,
        gym BOOLEAN NOT NULL,
        idioma TEXT,
        PRIMARY KEY(id, idioma)             
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarioRutina (
        idUsuari INTEGER PRIMARY KEY,
        nombreRutina TEXT NOT NULL,
        idRutina INTEGER NOT NULL,
        FOREIGN KEY(idRutina) REFERENCES tiposRutina(id),
        FOREIGN KEY(idUsuari) REFERENCES usuarios(id)             
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS textos (
        id INTEGER,
        idioma TEXT,
        infoTextos TEXT NOT NULL,
        PRIMARY KEY(id, idioma)       
    )
    ''')
    
    conexion.commit()
    conexion.close()
    print(f"Base de datos '{db_name}' creada con éxito.")

print(f"Base de datos '{db_name}' creada con éxito.")

# Funciones usuario
def addUsuario(id, nombre, edad, peso, idioma):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarios(id, nombre, edad, peso, idioma) 
        VALUES(?, ?, ?, ?, ?)
    ''', (id, nombre, edad, peso, idioma))
    conexion.commit()
    conexion.close()

def deleteUsuario(id):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()

# Funció per obtenir un usuari
def get_user(user_id):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conexion.close()
    return user

# Funciones rutina de usuario
def add_usuarioRutina(idUsuari, nombreRutina, idRutina):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarioRutina (idUsuari, nombreRutina, idRutina) 
        VALUES (?, ?, ?)
    ''', (idUsuari, nombreRutina, idRutina))
    conexion.commit()
    conexion.close()

def get_usuarioRutina(idUsuari):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarioRutina WHERE idUsuari = ?', (idUsuari,))
    user_routine = cursor.fetchone()
    conexion.close()
    return user_routine

def delete_usuarioRutina(idUsuario, idRutina):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM usuarioRutina WHERE idUsuari = ? AND idRutina = ?', (idUsuario, idRutina))
    conexion.commit()
    conexion.close()

# Funciones textos
def get_textos(id, idioma):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM textos WHERE id = ? AND idioma = ?', (id, idioma))
    text = cursor.fetchone()
    conexion.close()
    return text

# Funciones tipo de rutina
def get_tiposRutinas(id, idioma):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM tiposRutina WHERE id = ? AND idioma = ?', (id, idioma))
    rutinas = cursor.fetchone()
    conexion.close()
    return rutinas

def delete_tiposRutinas(id):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM tiposRutina WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()
