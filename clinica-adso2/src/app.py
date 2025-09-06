import sqlite3

from flask import Flask, g, jsonify, request

app = Flask(__name__)


# --- Conexion a SQLite ---
def bd_conexion():
    try:
        if 'conexion' not in g:
            g.conexion = sqlite3.connect("C:/Users/Julio/Desktop/clinica-adso/database/hospital.db")
        return g.conexion
    except Exception :
        return 'No hay conexión con la base de datos'

def cerrar_bd():
    conexion = g.pop('conexion', None)
    if conexion is not None:
        conexion.close()



@app.route('/')
def index():
    return '<h1>Utilizando Flask para el sistema Hospital</h1>'

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        sqlString = "SELECT * FROM tblUsuarios"
        conexion = bd_conexion()
        cursor = conexion.cursor()
        cursor.execute(sqlString)
        datos = cursor.fetchall()
        #print(datos)
        #return 'Usuarios en lista'
        usuarios = []
        for fila in datos:
            user = {'idUsuario': fila[0], 
                    'idTipoUsuario': fila[1], 
                    'Nombre': fila[2], 
                    'Apellido': fila[3], 
                    'FechaNacimiento': fila[4],
                    'Sexo': fila[5],
                    'TipoIdentificacion': fila[6],
                    'NumIdentificacion': fila[7],
                    'idEspecialidad': fila[8],
                    'Consultorio': fila[9],
                    'Direccion': fila[10],
                    'Telefono': fila[11],
                    'Correo': fila[12],
                    'Password': fila[13]
                    }
            usuarios.append(user)
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios en lista"})
    except Exception:
        return jsonify({'mensaje': "Error"})
    
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def listar_usuarios_id(id_usuario):
    try:
        conexion = bd_conexion()
        cursor = conexion.cursor()
        sqlString = "SELECT * FROM tblUsuarios WHERE idUsuario = '{0}'".format(id_usuario)
        cursor.execute(sqlString)
        datos = cursor.fetchone()
        if datos != None:
            user = {'idUsuario': datos[0], 
                    'idTipoUsuario': datos[1], 
                    'Nombre': datos[2], 
                    'Apellido': datos[3], 
                    'FechaNacimiento': datos[4],
                    'Sexo': datos[5],
                    'TipoIdentificacion': datos[6],
                    'NumIdentificacion': datos[7],
                    'idEspecialidad': datos[8],
                    'Consultorio': datos[9],
                    'Direccion': datos[10],
                    'Telefono': datos[11],
                    'Correo': datos[12],
                    'Password': datos[13]
                    }
            return jsonify({'usuarios': user, 'mensaje': "Usuarios en lista"})
        else:
            return jsonify({'mensaje': "Usuario no encontrado"})
    except Exception:
        return jsonify({'mensaje': "Error"})

@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        conexion = bd_conexion()
        cursor = conexion.cursor()
        sqlString = """INSERT INTO tblUsuarios (idUsuario, idTipoUsuario, Nombre, Apellido, FechaNacimiento, Sexo, TipoIdentificacion, NumIdentificacion, idEspecialidad, Consultorio, Direccion, Telefono, Correo, Password) 
        VALUES({0},{1},'{2}','{3}','{4}','{5}','{6}',{7},{8},{9},'{10}',{11},'{12}','{13}')""".format(request.json['idUsuario'], request.json['idTipoUsuario'],
                                                                                              request.json['Nombre'], request.json['Apellido'],
                                                                                              request.json['FechaNacimiento'], request.json['Sexo'],
                                                                                              request.json['TipoIdentificacion'], request.json['NumIdentificacion'],
                                                                                              request.json['idEspecialidad'], request.json['Consultorio'],
                                                                                              request.json['Direccion'], request.json['Telefono'], 
                                                                                              request.json['Correo'],request.json['Password'])
        cursor.execute(sqlString)
        conexion.commit()
        #print(request.json)
        return jsonify({'Mensaje': "Usuario registrado"})
    except Exception:
        return jsonify({'Mensaje': "Error"})
    

if (__name__ == '__main__'):
    app.run(debug=True)