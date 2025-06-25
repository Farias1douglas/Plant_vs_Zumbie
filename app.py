from flask import Flask, render_template, request
import json
from flask import flash, redirect
from utils import db
import os
from flask_migrate import Migrate
from models.Usuario import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdsadsaddsa'

db_path = "dbase/db.sqlite3"
if not db_path:
	raise RuntimeError("Environment variable 'DB_PATH' is not set.")
caminho_db = os.path.join(os.path.abspath(os.path.dirname(__file__)), db_path)
conexao = f'sqlite:///{caminho_db}'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)