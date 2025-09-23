from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import CSRFProtect

from config import config

import db

app = Flask(__name__)

csfr = CSRFProtect(app)
login_manager_app = LoginManager(app)

#-- Entidades
class Usuario(UserMixin):
    def __init__(self, id, nomusuario, password, nombre="") -> None:
        self.id = id
        self.nomusuario = nomusuario
        self.password = password
        self.nombre = nombre
     
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
 
#print(generate_password_hash("hola"))

#-- Modelos
class ModeloUsuario():
     
    @classmethod
    def login(self, usuario) -> None:
        try:
            con = db.conexion()
            cursor = con.cursor()
            sql = """SELECT id, nomusuario, password, nombre 
                     FROM tblUsuarios WHERE nomusuario = '{}'""".format(usuario.nomusuario)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                usuario = Usuario(row[0], row[1], Usuario.check_password(row[2], usuario.password), row[3])
                return usuario
            else:
                return None
        except Exception as ex:
            raise RuntimeError(ex)
    
    @classmethod
    def get_by_id(self, db, id) -> 'Usuario | None':
        try:
            con = db.conexion()
            cursor = con.cursor()
            sql = "SELECT id, nomusuario, nombre FROM tblUsuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Usuario(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise RuntimeError(ex)


@login_manager_app.user_loader #Crear este método para loguear y confirmar el usuario
def load_user(id):
    return ModeloUsuario.get_by_id(db, id)

            
#-- Endpoints --
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        #return render_template('/auth/login.html')
        usuario = Usuario(0,request.form['username'], request.form['password'])
        logged_user = ModeloUsuario.login(usuario)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Contraseña inválida')
                return render_template('auth/login.html')
        else:
            flash('Usuario no encontrado...')
            return render_template('/auth/login.html')
    else:
        return render_template('/auth/login.html')
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return '<h1>Es una vista protegida, sólo para usuarios autenticados!</h1>'

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return '<h1>Página no encontrada</h1>', 404
 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csfr.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
 