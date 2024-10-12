import sqlite3

# Nombre del fichero de la base de datos
db_name = "fitbot.db"

# Conectarse (esto también creará el archivo si no existe)
conexion = sqlite3.connect(db_name)

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear una tabla de ejemplo
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
    idUsuari INTEGER PRIMARY KEY,
    nombreRutina TEXT NOT NULL,
    idRutina INTEGER NOT NULL,
    FOREIGN KEY(idRutina) REFERENCES tiposRutina(id)
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

# Guardar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()

print(f"Base de datos '{db_name}' creada con éxito.")

#funciones usuario
def addUsuario(id, nombre, edad, peso, idioma):
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarios(id, nombre, edad, peso, idioma) 
        VALUES(?, ?, ?, ?, ?),
    ''', (id, nombre, edad, peso, idioma))
    conexion.commit()
    conexion.close()

def deleteUsuario(id):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id))
    conexion.commit()
    conexion.close()

def get_user(id):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id))
    user = cursor.fetchone()
    conexion.close()
    return user

#funciones rutina de usuario
def add_usuarioRutina(idUsuari, nombreRutina, idRutina):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarioRutina (idUsuari, nombreRutina, idRutina) 
        VALUES (?, ?, ?)
    ''', (idUsuari, nombreRutina, idRutina))
    conexion.commit()
    conexion.close()

def get_usuarioRutina(idUsuari):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarioRutina WHERE idUsuari = ?', (idUsuari))
    user_routine = cursor.fetchone()
    conexion.close()
    return user_routine

def delete_usuarioRutina(idUsuario, idRutina):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM usuarioRutina WHERE idUsuari = ? AND idRutina = ?', (idUsuario, idRutina))
    conexion.commit()
    conexion.close()


#funciones textos
def get_textos(id, idioma):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM textos WHERE id = ? AND idioma = ?', (id, idioma))
    text = cursor.fetchone()
    conexion.close()
    return text

#funciones tipo de rutina
def get_tiposRutinas(id, idioma):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM tiposRutina WHERE id = ? AND idioma = ?', (id, idioma))
    rutinas = cursor.fetchone()
    conexion.close()
    return rutinas

def add_tipoRutina(id, infoRutina, rango, gym, idioma):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    
    cursor.execute('''
        INSERT INTO tiposRutina (id, infoRutina, rango, gym, idioma) 
        VALUES (?, ?, ?, ?, ?)
    ''', (id, infoRutina, rango, gym, idioma))
    
    conexion.commit()
    conexion.close()

def get_next_rutina_id():
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    
    cursor.execute('SELECT MAX(id) FROM tiposRutina')
    result = cursor.fetchone()
    
    # Si no hi ha rutines, comencem per 1, sinó augmentem l'ID màxim en 1
    next_id = result[0] + 1 if result[0] else 1
    
    conexion.close()
    return next_id

def deleteUsuario(id):
    cursor = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM tiposRutina WHERE id = ?', (id))
    conexion.commit()
    conexion.close()

#Funciones tipo idioma

#Funcion getIdioma
def get_idioma(id_usuario):
    # Connexió a la base de dades
    conexion = sqlite3.connect('fitbot.db')
    cursor = conexion.cursor()
    
    # Recuperar l'idioma de l'usuari
    cursor.execute("SELECT idioma FROM usuarios WHERE id = ?", (id_usuario,))
    resultado = cursor.fetchone()
    
    conexion.close()

#Funcion UpdateIdioma and save idioma
def guardar_idioma_en_bd(id_usuario, idioma):
    conexion = sqlite3.connect('fitbot.db')
    cursor = conexion.cursor()
    
    # Actualitzar l'idioma per a l'usuari
    cursor.execute("UPDATE usuarios SET idioma = ? WHERE id = ?", (idioma, id_usuario))
    
    conexion.commit()
    conexion.close()

