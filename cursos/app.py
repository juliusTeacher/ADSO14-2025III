import sqlite3

from flask import Flask, flash, g, render_template, request, redirect, url_for


app = Flask(__name__)
app.secret_key = "clave123"

#---- Conexión a SQLite ---
def sql_connection():
    try:
        if 'con' not in g:
            g.con = sqlite3.connect("E:\\cursos\\database\\cursos.db")
        return g.con
    except Exception as Error:
        print(Error)

def close_db():
    con = g.pop( 'con', None )

    if con is not None:
        con.close()

#--- Fin a la conexión de SQLite ---

#-- Decorador 
@app.route('/cursos/add')
def add_curso():
    return render_template('cursos.html')

def pagina_no_encontrada(error):
    return '<h1>La página que intentas buscar no existe ... </h1>', 404


#-- Manejo de Endpoints

#-- Listar cursos
@app.route('/', methods=['GET', 'POST'])
def listar_cursos():
    con = sql_connection()
    cursor = con.cursor()
    
    if request.method == 'POST' and 'txtCodigo' in request.form:
        sqlString = "SELECT * FROM curso WHERE idCurso LIKE '%" + request.form['txtCodigo'] + "%'"
    else:
        sqlString = "SELECT * FROM curso"
    
    cursor.execute(sqlString)
    datos = cursor.fetchall()
    con.close()
    return render_template('lista.html', cursos=datos)

#-- Agregar cursos
@app.route('/cursos/add', methods=['POST'])
def guardar_cursos():
           
    codigo = request.form['txtCodigo']
    nombre = request.form['txtNombre']
    creditos = request.form['txtCreditos']
    
    con = sql_connection()
    cursor = con.cursor()
    cursor.execute('INSERT INTO curso (idCurso, nomCurso, creditos) VALUES(?, ?, ?)', (codigo, nombre, creditos))
    con.commit()
    con.close()
    
    return redirect('/')

#-- Editar cursos
@app.route('/editar/<int:codigo>', methods=['GET', 'POST'])
def editar_cursos(codigo):
    con = sql_connection()
    cursor = con.cursor()
    datos =  cursor.execute('SELECT * FROM curso WHERE idCurso =?',(codigo,)).fetchall()
    
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        creditos = request.form['txtCreditos']
        datos = cursor.execute('UPDATE curso SET nomCurso = ?, creditos = ? WHERE idCurso = ?', (nombre, creditos, codigo))
        con.commit()
        con.close()
        
        return redirect(url_for('listar_cursos'))
    
    return render_template('editar.html', curso=datos[0])

#-- Eliminar cursos: TAREA --> ¿Cómo anular un dato sin que elimine totalmente de la base de datos?
@app.route('/eliminar/<int:codigo>', methods=['GET', 'POST'])
def eliminar_cursos(codigo):
    con = sql_connection()
    cursor = con.cursor()
    if request.method == 'GET':
        cursor.execute('DELETE FROM curso WHERE idCurso = ?',(codigo,))
        con.commit()
        con.close()
        flash('Curso eliminado correctamente!')
        return redirect(url_for('listar_cursos'))
    
if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)