from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

app.config['JWT_SECRET_KEY'] = "claveSecreta"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lab'

mysql = MySQL(app)
jwt = JWTManager(app)

# registrar usuario
@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    codigo = data.get("codigo")
    nombre = data.get("nombre")
    email = data.get("email")
    rol = data.get("rol")
    carrera = data.get("carrera")
    departamento = data.get("departamento")
    telefono = data.get("telefono")
    password = data.get("password")

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO usuarios 
             (codigo, nombre, email, rol, carrera, departamento, telefono, password, activo) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)"""
    cursor.execute(sql, (codigo, nombre, email, rol, carrera, departamento, telefono, hashed_pw))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


# login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    codigo = data.get("codigo")
    password = data.get("password")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE codigo=%s", (codigo,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user["password"], password):
        token = create_access_token(identity=str(user["id"]))
        return jsonify({"token": token}), 200
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401


# edificios
@app.route('/edificios', methods=['GET'])
def listar_edificios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM edificios")
    edificios = cursor.fetchall()
    cursor.close()
    return jsonify(edificios),200

@app.route('/edificios', methods=['POST'])
@jwt_required()
def crear_edificio():
    data = request.get_json()
    nombre = data.get("nombre")
    direccion = data.get("direccion")
    telefono = data.get("telefono")

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO edificios(nombre, direccion, telefono) VALUES(%s, %s, %s)"
    cursor.execute(sql, (nombre, direccion, telefono))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    return jsonify({"mensaje": f"Edificio creado con id {nuevo_id}"}), 201

@app.route('/edificios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_edificio(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM edificios WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Edificio eliminado correctamente"})

@app.route('/edificios/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_edificio(id):
    data = request.get_json()
    nombre = data.get("nombre")
    direccion = data.get("direccion")
    telefono = data.get("telefono")

    cursor = mysql.connection.cursor()
    sql = """UPDATE edificios
             SET nombre=%s, direccion=%s, telefono=%s
             WHERE id=%s"""
    cursor.execute(sql, (nombre, direccion, telefono, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Edificio con id {id} actualizado correctamente"})
#usuario 
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)

@app.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_usuario(id):
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    rol = data.get("rol")
    carrera = data.get("carrera")
    departamento = data.get("departamento")
    telefono = data.get("telefono")
    activo = data.get("activo")

    cursor = mysql.connection.cursor()
    sql = """UPDATE usuarios
             SET nombre=%s, email=%s, rol=%s, carrera=%s, departamento=%s, telefono=%s, activo=%s
             WHERE id=%s"""
    cursor.execute(sql, (nombre, email, rol, carrera, departamento, telefono, activo, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Usuario con id {id} actualizado correctamente"})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Usuario eliminado correctamente"})

#laboratorios
@app.route('/laboratorios', methods=['GET'])
def listar_laboratorios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM laboratorios")
    laboratorios = cursor.fetchall()
    cursor.close()
    return jsonify(laboratorios)

@app.route('/laboratorios', methods=['POST'])
@jwt_required()
def crear_laboratorio():
    data = request.get_json()
    nombre = data.get("nombre")
    piso_id = data.get("piso_id")
    capacidad = data.get("capacidad")
    num_equipos = data.get("num_equipos")
    especialidad = data.get("especialidad")
    estado = data.get("estado")

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO laboratorios(nombre, piso_id, capacidad, num_equipos, especialidad, estado)
             VALUES(%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (nombre, piso_id, capacidad, num_equipos, especialidad, estado))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()

    return jsonify({"mensaje": f"Laboratorio creado con id {nuevo_id}"}), 201

@app.route('/laboratorios/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_laboratorio(id):
    data = request.get_json()
    nombre = data.get("nombre")
    piso_id = data.get("piso_id")
    capacidad = data.get("capacidad")
    num_equipos = data.get("num_equipos")
    especialidad = data.get("especialidad")
    estado = data.get("estado")

    cursor = mysql.connection.cursor()
    sql = """UPDATE laboratorios
             SET nombre=%s, piso_id=%s, capacidad=%s, num_equipos=%s, especialidad=%s, estado=%s
             WHERE id=%s"""
    cursor.execute(sql, (nombre, piso_id, capacidad, num_equipos, especialidad, estado, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Laboratorio con id {id} actualizado correctamente"})

@app.route('/laboratorios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_laboratorio(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM laboratorios WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Laboratorio eliminado correctamente"})


#pisos
@app.route('/pisos', methods=['GET'])
def listar_pisos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pisos")
    pisos = cursor.fetchall()
    cursor.close()
    return jsonify(pisos),200

@app.route('/pisos', methods=['POST'])
@jwt_required()
def crear_piso():
    data = request.get_json()
    numero = data.get("numero")
    edificio_id = data.get("edificio_id")

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO pisos(numero, edificio_id) VALUES(%s, %s)"
    cursor.execute(sql, (numero, edificio_id))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()

    return jsonify({"mensaje": f"Piso creado con id {nuevo_id}"}), 201

@app.route('/pisos/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_piso(id):
    data = request.get_json()
    numero = data.get("numero")
    edificio_id = data.get("edificio_id")

    cursor = mysql.connection.cursor()
    sql = """UPDATE pisos
             SET numero=%s, edificio_id=%s
             WHERE id=%s"""
    cursor.execute(sql, (numero, edificio_id, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Piso con id {id} actualizado correctamente"}), 200


@app.route('/pisos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_pisos(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM pisos WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "piso eliminado correctamente"})

#Equipos
@app.route('/equipos', methods=['GET'])
def listar_equipos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    cursor.close()
    return jsonify(equipos),200

@app.route('/equipos', methods=['POST'])
@jwt_required()
def crear_equipos():
    data = request.get_json()
    codigo = data.get("codigo")
    laboratorio_id = data.get("laboratorio_id")
    tipo = data.get("tipo")
    marca = data.get("marca")
    modelo = data.get("modelo")
    estado = data.get("estado")

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO pisos(codigo, laboratorio_id, tipo, marca, modelo, estado) VALUES(%s, %s,%s, %s,%s, %s)"
    cursor.execute(sql, (codigo, laboratorio_id,tipo, marca, modelo, estado ))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()

    return jsonify({"mensaje": f"equipo creado con id {nuevo_id}"}), 201

@app.route('/equipos/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_equipo(id):
    data = request.get_json()
    codigo = data.get("codigo")
    laboratorio_id = data.get("laboratorio_id")
    tipo = data.get("tipo")
    marca = data.get("marca")
    modelo = data.get("modelo")
    estado = data.get("estado")

    cursor = mysql.connection.cursor()
    sql = """UPDATE equipos
             SET codigo=%s, laboratorio_id=%s, tipo=%s, marca=%s, modelo=%s, estado=%s
             WHERE id=%s"""
    cursor.execute(sql, (codigo, laboratorio_id, tipo, marca, modelo, estado, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Equipo con id {id} actualizado correctamente"}), 200


@app.route('/equipos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_equipos(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM equipos WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "equipo eliminado correctamente"})

#reservas
@app.route('/reservas', methods=['GET'])
@jwt_required()
def listar_reservas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    return jsonify(reservas), 200

@app.route('/reservas', methods=['POST'])
@jwt_required()
def crear_reserva():
    data = request.get_json()
    laboratorio_id = data.get("laboratorio_id")
    usuario_id = data.get("usuario_id")
    fecha = data.get("fecha")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    motivo = data.get("motivo")
    estado = data.get("estado", "pendiente")

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO reservas(laboratorio_id, usuario_id, fecha, hora_inicio, hora_fin, motivo, estado)
             VALUES(%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (laboratorio_id, usuario_id, fecha, hora_inicio, hora_fin, motivo, estado))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()

    return jsonify({"mensaje": f"Reserva creada con id {nuevo_id}"}), 201

@app.route('/reservas/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_reserva(id):
    data = request.get_json()
    estado = data.get("estado")
    aprobado_por = data.get("aprobado_por")
    comentario_admin = data.get("comentario_admin")

    cursor = mysql.connection.cursor()
    sql = """UPDATE reservas
             SET estado=%s, aprobado_por=%s, comentario_admin=%s, fecha_aprobacion=NOW()
             WHERE id=%s"""
    cursor.execute(sql, (estado, aprobado_por, comentario_admin, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Reserva con id {id} actualizada correctamente"}), 200

@app.route('/reservas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_reserva(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM reservas WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Reserva eliminada correctamente"}), 200

#Incidencia
@app.route('/incidencias', methods=['GET'])
@jwt_required()
def listar_incidencias():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM incidencias")
    incidencias = cursor.fetchall()
    cursor.close()
    return jsonify(incidencias), 200

@app.route('/incidencias', methods=['POST'])
@jwt_required()
def crear_incidencia():
    data = request.get_json()
    laboratorio_id = data.get("laboratorio_id")
    equipo_id = data.get("equipo_id")
    usuario_id = data.get("usuario_id")
    tipo = data.get("tipo")
    descripcion = data.get("descripcion")
    prioridad = data.get("prioridad", "media")
    estado = data.get("estado", "reportada")

    cursor = mysql.connection.cursor()
    sql = """INSERT INTO incidencias(laboratorio_id, equipo_id, usuario_id, tipo, descripcion, prioridad, estado)
             VALUES(%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (laboratorio_id, equipo_id, usuario_id, tipo, descripcion, prioridad, estado))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()

    return jsonify({"mensaje": f"Incidencia creada con id {nuevo_id}"}), 201

@app.route('/incidencias/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_incidencia(id):
    data = request.get_json()
    estado = data.get("estado")
    prioridad = data.get("prioridad")

    cursor = mysql.connection.cursor()
    sql = """UPDATE incidencias
             SET estado=%s, prioridad=%s
             WHERE id=%s"""
    cursor.execute(sql, (estado, prioridad, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje": f"Incidencia con id {id} actualizada correctamente"}), 200

@app.route('/incidencias/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_incidencia(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM incidencias WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Incidencia eliminada correctamente"}), 200



if __name__ == "__main__":
    app.run(debug=True)
