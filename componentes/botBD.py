import sqlite3

# Nombre del fitxer de la base de dades
db_name = "fitbot.db"

# Connectar-se (això també crearà el fitxer si no existeix)
with sqlite3.connect(db_name) as conexion:
    # Crear un cursor per executar comandes SQL
    cursor = conexion.cursor()

    # Crear una taula d'exemple
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL CHECK (edad >= 0 AND edad <= 120),
        peso FLOAT NOT NULL,
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
        idUsuari INTEGER,
        nombreRutina TEXT NOT NULL,
        idRutina INTEGER NOT NULL,
        FOREIGN KEY(idRutina) REFERENCES tiposRutina(id),
        FOREIGN KEY(idUsuari) REFERENCES usuarios(id), 
        PRIMARY KEY(idUsuari, idRutina)  -- Afegit clau primària
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

    # Guardar els canvis
    conexion.commit()
print(f"Base de dades '{db_name}' creada amb èxit.")

# Funcions d'usuari
def addUsuario(id, nombre, edad, peso, idioma):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO usuarios (id, nombre, edad, peso, idioma) 
                          VALUES (?, ?, ?, ?, ?)''', (id, nombre, edad, peso, idioma))
        conexion.commit()

def deleteUsuario(id):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conexion.commit()

def get_user(id):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
        user = cursor.fetchone()
    return user

# Funcions rutina d'usuari
def add_usuarioRutina(idUsuari, nombreRutina, idRutina):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO usuarioRutina (idUsuari, nombreRutina, idRutina) 
                          VALUES (?, ?, ?)''', (idUsuari, nombreRutina, idRutina))
        conexion.commit()

def get_usuarioRutina(idUsuari):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM usuarioRutina WHERE idUsuari = ?', (idUsuari,))
        user_routine = cursor.fetchall()  # Utilitzar fetchall per obtenir totes les rutines
    return user_routine

def delete_usuarioRutina(idUsuario, idRutina):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM usuarioRutina WHERE idUsuari = ? AND idRutina = ?', (idUsuario, idRutina))
        conexion.commit()

# Funcions textos
def get_textos(id, idioma):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM textos WHERE id = ? AND idioma = ?', (id, idioma))
        text = cursor.fetchone()
    return text

# Funcions tipus rutina
def get_tiposRutinas(id, idioma):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM tiposRutina WHERE id = ? AND idioma = ?', (id, idioma))
        rutinas = cursor.fetchone()
    return rutinas

def add_tipoRutina(id, infoRutina, rango, gym, idioma):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO tiposRutina (id, infoRutina, rango, gym, idioma) 
                          VALUES (?, ?, ?, ?, ?)''', (id, infoRutina, rango, gym, idioma))
        conexion.commit()

def get_next_rutina_id():
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('SELECT MAX(id) FROM tiposRutina')
        result = cursor.fetchone()
        next_id = result[0] + 1 if result[0] else 1
    return next_id

def deleteTipoRutina(id):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM tiposRutina WHERE id = ?', (id,))
        conexion.commit()

# Funcions idioma
def get_idioma(id_usuario):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT idioma FROM usuarios WHERE id = ?", (id_usuario,))
        resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def guardar_idioma_en_bd(id_usuario, idioma):
    with sqlite3.connect(db_name) as conexion:
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET idioma = ? WHERE id = ?", (idioma, id_usuario))
        conexion.commit()