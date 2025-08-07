from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from utils import db
import os
from flask_migrate import Migrate
from models.models import Usuario

app = Flask(__name__)
lm = LoginManager(app)
lm.login_view = 'login_usuario'
app.secret_key= 'douglastestando'

@lm.user_loader
def user_loader(id): 
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario

db_path = "dbase/db.sqlite3"
if not db_path:
	raise RuntimeError("Environment variable 'DB_PATH' is not set.")
caminho_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_path)
conexao = f'sqlite:///{caminho_db}'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

#the zombies are coming...#
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/faleconosco')
@login_required
def faleconosco():
    return render_template('contato.html')
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/comentarios')
@login_required
def comentarios():
    return render_template('comentarios.html')
#---------------------------------------------------
@app.route('/jardimdia')
def jardimdia():
    return render_template('jardim-dia.html')
@app.route('/jardimnoite')
def jardimnoite():
    return render_template('jardim-noite.html')
@app.route('/piscinadia')
def piscinadodia():
    return render_template('piscina-dia.html')
@app.route('/piscinanoite')
def piscinanite():
    return render_template('piscina-noite.html')
@app.route('/telhadodia')
def telhadodia():
    return render_template('telhado-dia.html')
@app.route('/telhadonoite')
def telhadonoite():
    return render_template('telhado-noite.html')
@app.route('/nevoa')
def nevoa():
    return render_template('nevoa.html')
@app.route('/itens')
def itens():
    return render_template('itens.html')

#brains...#
@app.route('/login', methods=['POST', 'GET'])
def login_usuario():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form('email')
        senha = request.form('senha')

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()
        if not usuario:
            return "Usuário ou senha inválidos", 401
        if usuario:
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            return "Usuário ou senha inválidos", 401
@app.route('/cadastro', methods=['POST', 'GET'])
def recebedados():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        person = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(person)
        db.session.commit()

        login_user(person)

        return redirect(url_for('home'))
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#lingua do dave maluco#
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)