import os
from flask.helpers import flash
from werkzeug.utils import secure_filename
from forms.forms import *
from flask import Flask, render_template, url_for, redirect, jsonify,request
from db import *

UPLOAD_FOLDER = os.path.abspath("static/imagenes/imgpub")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET', 'POST'])
def index():
    form = PublicacionForm()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        
        db = get_db()
        db.execute('INSERT INTO publicacion (titulo, descripcion, url) VALUES (?,?,?)', (titulo, descripcion,filename))
        db.commit()
        return redirect(url_for("index"))
    db=get_db()
    cursorObj = db.cursor()
    cursorObj.execute("SELECT * FROM publicacion")
    publicacion = cursorObj.fetchall()

    return render_template('index.html',form=form,publicacion=publicacion)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form=LoginForm(request.form)
    if request.method == 'POST':
        if request.form['btn'] == 'Iniciar':
 
            return redirect(url_for('index'))
        elif request.form['btn'] == 'Registro':
            return redirect(url_for('registro'))

    elif request.method == 'GET':
        return render_template('login.html',form=form) 
    

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    
    if(form.validate_on_submit()):
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():

    db=get_db()
    cursorObj = db.cursor()
    cursorObj.execute("SELECT * FROM publicacion")
    publicacion = cursorObj.fetchall()
    
    return render_template('perfil.html',publicacion=publicacion)

@app.route('/detalle', methods=['GET', 'POST'])
def detalle():
    
    return render_template('detalle.html')

@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    
    return render_template('busqueda.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)