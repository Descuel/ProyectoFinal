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
        token = create_access_token(identity=user["id"])
        return jsonify({"token": token}), 200
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

# edificios
@app.route('/edificios', methods=['GET'])
def listar_edificios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM edificios")
    edificios = cursor.fetchall()
    cursor.close()
    return jsonify(edificios)

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

if __name__ == "__main__":
    app.run(debug=True)
