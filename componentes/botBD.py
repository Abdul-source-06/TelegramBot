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
    edad INTEGER NOT NULL,
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
    idRutina INTEGER NOT NULL       
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