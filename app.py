from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import MySQLdb
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================
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

# ============================================
# RUTAS PARA PÁGINAS HTML (FRONTEND)
# ============================================
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/registro')
def registro_page():
    return render_template('registro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-usuario')
def dashboard_usuario():
    return render_template('dashboard_usuario.html')

@app.route('/edificios-admin')
def edificios_page():
    return render_template('edificios.html')

@app.route('/laboratorios-admin')
def laboratorios_page():
    return render_template('laboratorios.html')

@app.route('/equipos-gestion')
def equipos_gestion():
    return render_template('equipos_admin.html')

@app.route('/reservas-admin')
def reservas_admin():
    return render_template('reservas_admin.html')

@app.route('/incidencias-admin')
def incidencias_admin():
    return render_template('incidencias_admin.html')

@app.route('/usuarios-admin')
def usuarios_admin():
    return render_template('usuarios_admin.html')

# ============================================
# AUTENTICACIÓN Y USUARIOS
# ============================================

# Registro de nuevos usuarios (docente/estudiante) – SIN TOKEN (público)
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

# Inicio de sesión (devuelve token JWT y el rol del usuario)
@app.route('/api/login', methods=['POST'])
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
        return jsonify({"token": token, "rol": user["rol"]}), 200
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

# Obtener perfil del usuario autenticado (requiere token)
@app.route('/usuarios/perfil', methods=['GET'])
@jwt_required()
def perfil_usuario():
    user_id = get_jwt_identity()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, codigo, nombre, email, rol FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return jsonify(user), 200

# CRUD de Usuarios (listar, actualizar, eliminar)
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios), 200

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

@app.route('/usuarios/<int:id>/cambiar-password', methods=['PUT'])
@jwt_required()
def cambiar_password_usuario(id):
    data = request.get_json()
    nueva_password = data.get("password")
    if not nueva_password:
        return jsonify({"mensaje": "La contraseña es obligatoria"}), 400
    hashed_pw = bcrypt.generate_password_hash(nueva_password).decode('utf-8')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET password = %s WHERE id = %s", (hashed_pw, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Contraseña actualizada correctamente"}), 200

# ============================================
# CRUD DE EDIFICIOS
# ============================================
@app.route('/edificios', methods=['GET'])
def listar_edificios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM edificios")
    edificios = cursor.fetchall()
    cursor.close()
    return jsonify(edificios), 200

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

@app.route('/edificios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_edificio(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM edificios WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Edificio eliminado correctamente"})

# ============================================
# CRUD DE PISOS
# ============================================
@app.route('/pisos', methods=['GET'])
def listar_pisos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pisos")
    pisos = cursor.fetchall()
    cursor.close()
    return jsonify(pisos), 200

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
def eliminar_piso(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM pisos WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Piso eliminado correctamente"})

# ============================================
# CRUD DE LABORATORIOS
# ============================================
@app.route('/laboratorios', methods=['GET'])
def listar_laboratorios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM laboratorios")
    laboratorios = cursor.fetchall()
    cursor.close()
    return jsonify(laboratorios), 200

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

# ============================================
# CRUD DE EQUIPOS
# ============================================
@app.route('/equipos', methods=['GET'])
def listar_equipos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    cursor.close()
    return jsonify(equipos), 200

@app.route('/equipos', methods=['POST'])
@jwt_required()
def crear_equipo():
    data = request.get_json()
    codigo = data.get("codigo")
    laboratorio_id = data.get("laboratorio_id")
    tipo = data.get("tipo")
    marca = data.get("marca")
    modelo = data.get("modelo")
    estado = data.get("estado", "operativo")
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO equipos(codigo, laboratorio_id, tipo, marca, modelo, estado) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (codigo, laboratorio_id, tipo, marca, modelo, estado))
    mysql.connection.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    return jsonify({"mensaje": f"Equipo creado con id {nuevo_id}"}), 201

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
def eliminar_equipo(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM equipos WHERE id=%s"
    cursor.execute(sql, (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"mensaje": "Equipo eliminado correctamente"})

# ============================================
# CRUD DE RESERVAS (con aprobación)
# ============================================
@app.route('/reservas', methods=['GET'])
@jwt_required()
def listar_reservas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    for r in reservas:
        if 'hora_inicio' in r and r['hora_inicio'] is not None:
            r['hora_inicio'] = str(r['hora_inicio'])
        if 'hora_fin' in r and r['hora_fin'] is not None:
            r['hora_fin'] = str(r['hora_fin'])
        if 'fecha_aprobacion' in r and r['fecha_aprobacion'] is not None:
            r['fecha_aprobacion'] = str(r['fecha_aprobacion'])
        if 'created_at' in r and r['created_at'] is not None:
            r['created_at'] = str(r['created_at'])
    return jsonify(reservas), 200

@app.route('/reservas', methods=['POST'])
@jwt_required()
def crear_reserva():
    data = request.get_json()
    laboratorio_id = data.get("laboratorio_id")
    fecha = data.get("fecha")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    motivo = data.get("motivo")
    estado = data.get("estado", "pendiente")
    usuario_id = get_jwt_identity()
    if not laboratorio_id or not fecha or not hora_inicio or not hora_fin:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400
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

@app.route('/mis-reservas', methods=['GET'])
@jwt_required()
def mis_reservas_endpoint():
    user_id = get_jwt_identity()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """SELECT r.*, l.nombre as laboratorio_nombre 
             FROM reservas r
             JOIN laboratorios l ON r.laboratorio_id = l.id
             WHERE r.usuario_id = %s
             ORDER BY r.fecha DESC, r.hora_inicio ASC"""
    cursor.execute(sql, (user_id,))
    reservas = cursor.fetchall()
    cursor.close()
    for r in reservas:
        if 'hora_inicio' in r and r['hora_inicio'] is not None:
            r['hora_inicio'] = str(r['hora_inicio'])
        if 'hora_fin' in r and r['hora_fin'] is not None:
            r['hora_fin'] = str(r['hora_fin'])
    return jsonify(reservas), 200

# ============================================
# CRUD DE INCIDENCIAS
# ============================================
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
    tipo = data.get("tipo")
    descripcion = data.get("descripcion")
    prioridad = data.get("prioridad", "media")
    estado = data.get("estado", "reportada")
    usuario_id = get_jwt_identity()
    if not laboratorio_id or not tipo or not descripcion:
        return jsonify({"mensaje": "Faltan datos"}), 400
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

# ============================================
# ESTADÍSTICAS PARA EL DASHBOARD (según rol)
# ============================================
@app.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def dashboard_stats():
    user_id = get_jwt_identity()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    stats = {"rol": user['rol']}
    if user['rol'] == 'admin':
        cursor.execute("SELECT COUNT(*) as total FROM laboratorios")
        stats['total_laboratorios'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM equipos")
        stats['total_equipos'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE estado = 'pendiente'")
        stats['reservas_pendientes'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        stats['total_usuarios'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM incidencias WHERE estado != 'resuelta'")
        stats['incidencias_pendientes'] = cursor.fetchone()['total']
    else:
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE usuario_id = %s", (user_id,))
        stats['mis_reservas'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE usuario_id = %s AND estado = 'aprobada'", (user_id,))
        stats['reservas_aprobadas'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE usuario_id = %s AND estado = 'pendiente'", (user_id,))
        stats['reservas_pendientes'] = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM incidencias WHERE usuario_id = %s", (user_id,))
        stats['mis_incidencias'] = cursor.fetchone()['total']
    cursor.close()
    return jsonify(stats), 200

# ============================================
# CONSULTA PERSONALIZADA (REQUISITO 6)
# ============================================
@app.route('/disponibilidad', methods=['GET'])
def disponibilidad_laboratorios():
    fecha = request.args.get('fecha')
    hora_inicio = request.args.get('hora_inicio', '00:00')
    hora_fin = request.args.get('hora_fin', '23:59')
    if not fecha:
        return jsonify({"error": "Se requiere fecha (formato YYYY-MM-DD)"}), 400
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT l.*, e.nombre AS edificio_nombre
        FROM laboratorios l
        JOIN pisos p ON l.piso_id = p.id
        JOIN edificios e ON p.edificio_id = e.id
        WHERE l.id NOT IN (
            SELECT r.laboratorio_id FROM reservas r
            WHERE r.fecha = %s 
            AND r.estado IN ('aprobada', 'pendiente')
            AND (
                (r.hora_inicio <= %s AND r.hora_fin > %s) OR
                (r.hora_inicio < %s AND r.hora_fin >= %s) OR
                (r.hora_inicio >= %s AND r.hora_fin <= %s)
            )
        )
        AND l.estado = 'disponible'
    """
    cursor.execute(sql, (fecha, hora_inicio, hora_inicio, hora_fin, hora_fin, hora_inicio, hora_fin))
    disponibles = cursor.fetchall()
    cursor.close()
    return jsonify({
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "laboratorios_disponibles": disponibles
    }), 200

# ============================================
# VISTAS SQL (consultas predefinidas)
# ============================================
@app.route('/api/vistas/capacidad-pisos', methods=['GET'])
def get_capacidad_pisos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM vista_capacidad_pisos")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data), 200

@app.route('/api/vistas/ocupacion-laboratorios', methods=['GET'])
def get_ocupacion_laboratorios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM vista_laboratorios_ocupacion")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data), 200

@app.route('/api/vistas/incidencias-pendientes', methods=['GET'])
@jwt_required()
def get_incidencias_pendientes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM vista_incidencias_pendientes")
    data = cursor.fetchall()
    cursor.close()
    return jsonify(data), 200

# ============================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================
if __name__ == "__main__":
    app.run(debug=True)